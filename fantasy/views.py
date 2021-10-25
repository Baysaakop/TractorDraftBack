from rest_framework import status
from rest_framework.response import Response
from .models import Career, Manager, Match, Gameweek, TableTeam, Table, League, Duel, League19Team, League19, Post
from .serializers import ManagerSerializer, MatchSerializer, GameweekSerializer, TableTeamSerializer, TableSerializer, LeagueSerializer, DuelSerializer, League19Serializer, League19TeamSerializer, PostSerializer
from rest_framework import viewsets
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters


class ManagerViewSet(viewsets.ModelViewSet):
    serializer_class = ManagerSerializer
    queryset = Manager.objects.all()


class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()
    # def update(self, request, pk=None):
    #     instance = self.get_object()
    #     updateLeague(instance.id)
    #     return super().update(request)


class GameweekViewSet(viewsets.ModelViewSet):
    serializer_class = GameweekSerializer
    queryset = Gameweek.objects.all()

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        update(instance, request.data)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # Do ViewSet work.
        self.perform_update(serializer)
        return Response(serializer.data)


class TableTeamViewSet(viewsets.ModelViewSet):
    serializer_class = TableTeamSerializer
    queryset = TableTeam.objects.all()


class TableViewSet(viewsets.ModelViewSet):
    serializer_class = TableSerializer
    queryset = Table.objects.all()


class LeagueViewSet(viewsets.ModelViewSet):
    serializer_class = LeagueSerializer
    queryset = League.objects.all()

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        if 'finish' in request.data:
            finish(instance)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # Do ViewSet work.
        self.perform_update(serializer)
        return Response(serializer.data)


class DuelViewSet(viewsets.ModelViewSet):
    serializer_class = DuelSerializer
    queryset = Duel.objects.all()


class League19TeamViewSet(viewsets.ModelViewSet):
    serializer_class = League19TeamSerializer
    queryset = League19Team.objects.all()


class League19ViewSet(viewsets.ModelViewSet):
    serializer_class = League19Serializer
    queryset = League19.objects.all()


def update(gameweek, data):
    league = League.objects.get(gameweeks=gameweek)
    table = league.table
    teams = table.teams.all()
    scores = []
    for d in data['matches']:
        # Update Match
        match = Match.objects.get(id=d['id'])
        home_score = d['home_score']
        away_score = d['away_score']
        scores.append(home_score)
        scores.append(away_score)
        match.home_score = home_score
        match.away_score = away_score
        match.save()
        home_team = match.home_team
        away_team = match.away_team
        # Update table team
        home_tableteam = teams.get(manager=home_team)
        away_tableteam = teams.get(manager=away_team)
        home_tableteam.score += home_score
        away_tableteam.score += away_score
        home_tableteam.score_away += away_score
        away_tableteam.score_away += home_score
        if home_score > away_score:
            home_tableteam.wins += 1
            away_tableteam.losses += 1
            home_tableteam.points += 3
        elif away_score > home_score:
            away_tableteam.wins += 1
            home_tableteam.losses += 1
            away_tableteam.points += 3
        else:
            home_tableteam.draws += 1
            away_tableteam.draws += 1
            home_tableteam.points += 1
            away_tableteam.points += 1
        home_tableteam.save()
        away_tableteam.save()
        duel = None
        duels = Duel.objects.filter(Q(team1=match.home_team, team2=match.away_team) | Q(
            team2=match.home_team, team1=match.away_team))
        if not duels:
            duel = Duel.objects.create(
                team1=match.home_team, team2=match.away_team)
        else:
            duel = duels[0]
        if duel.team1 == match.home_team:
            if match.home_score > match.away_score:
                duel.win1 += 1
            elif match.away_score > match.home_score:
                duel.win2 += 1
            else:
                duel.draw += 1
        else:
            if match.home_score > match.away_score:
                duel.win2 += 1
            elif match.away_score > match.home_score:
                duel.win1 += 1
            else:
                duel.draw += 1
        duel.save()
    gameweek.save()
    # Update top scorer
    matches = gameweek.matches.all().filter(
        Q(home_score=max(scores)) | Q(away_score=max(scores)))
    for match in matches:
        if match.home_score > match.away_score:
            winner = teams.get(manager=match.home_team)
            winner.topscorer += 1
            loser = teams.get(manager=match.away_team)
            loser.topscorer_away += 1
            winner.save()
            loser.save()
        elif match.away_score > match.home_score:
            winner = teams.get(manager=match.away_team)
            winner.topscorer += 1
            loser = teams.get(manager=match.home_team)
            loser.topscorer_away += 1
            winner.save()
            loser.save()
        else:
            player1 = teams.get(manager=match.home_team)
            player2 = teams.get(manager=match.away_team)
            player1.topscorer += 1
            player2.topscorer += 1
            player1.topscorer_away += 1
            player2.topscorer_away += 1
            player1.save()
            player2.save()
    setRanks(teams)


def setRanks(teams):
    rank = 1
    for team in teams.order_by('-points', '-score'):
        team.rank = rank
        rank = rank + 1
        team.save()


def finish(league):
    table = league.table
    teams = table.teams.all()
    updateCareer(teams)


def updateCareer(teams, level):
    for team in teams:
        manager = team.manager
        career, created = Career.objects.get_or_create(
            manager=manager, level=level)
        career.total_point += team.points
        career.total_win += team.wins
        career.total_draw += team.draws
        career.total_loss += team.losses
        career.total_score += team.score
        career.total_score_away += team.score_away
        career.total_topscorer += team.topscorer
        career.total_topscorer_away += team.topscorer_away
        career.total_vanga += team.vanga
        career.total_appearance += 1
        career.total_match += 9
        if team.rank == 1:
            career.total_champion += 1
        elif team.rank == 2:
            career.total_runnerup += 1
        elif team.rank == 3:
            career.total_third += 1
        career.save()


def resetTeams(teams):
    for team in teams:
        team.rank = 0
        team.score = 0
        team.score_away = 0
        team.points = 0
        team.wins = 0
        team.draws = 0
        team.losses = 0
        team.topscorer = 0
        team.topscorer_away = 0
        team.save()


def resetCareer(teams, level):
    for team in teams:
        manager = team.manager
        careers = manager.career.filter(level=level)
        if not careers:
            career = Career.objects.create(
                level=level
            )
            career.save()
            manager.career.add(career)
        else:
            career = careers[0]
            career.total_point = 0
            career.total_win = 0
            career.total_draw = 0
            career.total_loss = 0
            career.total_score = 0
            career.total_score_away = 0
            career.total_appearance = 0
            career.total_match = 0
            career.total_topscorer = 0
            career.total_topscorer_away = 0
            career.total_vanga = 0
            career.save()
            manager.save()


def setCareer(teams, level):
    for team in teams:
        manager = team.manager
        careers = manager.career.filter(level=level)
        career = careers[0]
        seasons = League.objects.filter(level=level)
        for season in seasons:
            table = season.table
            tableteams = table.teams.all()
            for tableteam in tableteams:
                if (tableteam.manager == manager):
                    career.total_point += tableteam.points
                    career.total_win += tableteam.wins
                    career.total_draw += tableteam.draws
                    career.total_loss += tableteam.losses
                    career.total_score += tableteam.score
                    career.total_score_away += tableteam.score_away
                    career.total_topscorer += tableteam.topscorer
                    career.total_topscorer_away += tableteam.topscorer_away
                    career.total_vanga += tableteam.vanga
                    career.total_match += (tableteam.wins +
                                           tableteam.draws + tableteam.losses)
                    if ((tableteam.wins + tableteam.draws + tableteam.losses) == 9):
                        career.total_appearance += 1
        career.save()
        manager.save()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.order_by('-created_at')
