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
    # Update Match
    for d in data['matches']:
        match = Match.objects.get(id=d['id'])
        home_score = d['home_score']
        away_score = d['away_score']
        match.home_score = home_score
        match.away_score = away_score
        match.save()
        home_team = match.home_team
        away_team = match.away_team
        duels = Duel.objects.filter(
            Q(team1=home_team, team2=away_team) | Q(team1=away_team, team2=home_team))
        if not duels:
            duel = Duel.objects.create(
                team1=home_team,
                team2=away_team
            )
            if (home_score > away_score):
                duel.win1 += 1
            elif (home_score < away_score):
                duel.win2 += 1
            else:
                duel.draw += 1
            duel.save()
        else:
            duel = duels[0]
            if (duel.team1 == home_team):
                if (home_score > away_score):
                    duel.win1 += 1
                elif (home_score < away_score):
                    duel.win2 += 1
                else:
                    duel.draw += 1
            else:
                if (away_score > home_score):
                    duel.win1 += 1
                elif (away_score < home_score):
                    duel.win2 += 1
                else:
                    duel.draw += 1
            duel.save()
    gameweek.save()
    # Update Table Team
    resetTeams(teams)
    for week in league.gameweeks.all():
        scores = []
        for ma in week.matches.all():
            scores.append(ma.home_score)
            scores.append(ma.away_score)
        for m in week.matches.all():
            if (m.home_score > 0 and m.away_score > 0):
                home_team = teams.get(manager=m.home_team)
                away_team = teams.get(manager=m.away_team)
                home_team.score += m.home_score
                home_team.score_away += m.away_score
                away_team.score += m.away_score
                away_team.score_away += m.home_score
                if (m.home_score > m.away_score):
                    home_team.wins = home_team.wins + 1
                    away_team.losses = away_team.losses + 1
                    home_team.points = home_team.points + 3
                elif (m.home_score < m.away_score):
                    away_team.wins = away_team.wins + 1
                    home_team.losses = home_team.losses + 1
                    away_team.points = away_team.points + 3
                else:
                    home_team.draws = home_team.draws + 1
                    away_team.draws = away_team.draws + 1
                    home_team.points = home_team.points + 1
                    away_team.points = away_team.points + 1
                if (m.home_score == max(scores)):
                    home_team.topscorer += 1
                    away_team.topscorer_away += 1
                if (m.away_score == max(scores)):
                    away_team.topscorer += 1
                    home_team.topscorer_away += 1
                home_team.save()
                away_team.save()
    # Set ranks
    setRanks(teams)
    resetCareer(teams, league.level)
    setCareer(teams, league.level)


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


def setRanks(teams):
    rank = 1
    for team in teams.order_by('-points', '-score'):
        team.rank = rank
        rank = rank + 1
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
