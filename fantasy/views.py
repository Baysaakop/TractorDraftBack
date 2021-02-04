from rest_framework import status
from rest_framework.response import Response
from .models import Career, Manager, Match, Gameweek, TableTeam, Table, League, Duel, League19Team, League19
from .serializers import ManagerSerializer, MatchSerializer, GameweekSerializer, TableTeamSerializer, TableSerializer, LeagueSerializer, DuelSerializer, League19Serializer, League19TeamSerializer
from rest_framework import viewsets
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

class ManagerViewSet(viewsets.ModelViewSet):
    serializer_class = ManagerSerializer
    queryset = Manager.objects.all()

    def update(self, request, pk=None):
        instance = self.get_object()
        updateCareer(instance.id)
        return super().update(request)

class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()

    def update(self, request, pk=None):
        instance = self.get_object()
        updateLeague(instance.id)
        return super().update(request)

class GameweekViewSet(viewsets.ModelViewSet):
    serializer_class = GameweekSerializer
    queryset = Gameweek.objects.all()

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

def updateLeague(id):
    match = Match.objects.get(pk=id)
    gm = Gameweek.objects.get(matches=match)
    league = League.objects.get(gameweeks=gm)
    table = league.table
    tableteams = table.teams.all()           
    resetTeams(tableteams)
    for week in league.gameweeks.all():
        for m in week.matches.all():
            home_team = tableteams.get(manager=m.home_team)
            away_team = tableteams.get(manager=m.away_team)   
            home_team.score = home_team.score + m.home_score
            away_team.score = away_team.score + m.away_score       
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
            home_team.save()
            away_team.save()            
    
def resetTeams(teams):
    for team in teams: 
        team.rank = 0       
        team.score = 0
        team.points = 0
        team.wins = 0
        team.draws = 0
        team.losses = 0
        team.save()

def setRanks(teams):    
    mylist = sorted(teams, key=lambda x: (x.points, x.score))
    rank = 10
    for team in mylist: 
        team.rank = rank        
        rank = rank - 1
        team.save()
            

# def updateCareer(id):
#     manager = Manager.objects.get(pk=id)    
#     teams = TableTeam.objects.filter(manager=manager)
#     for team in teams:
#         table = Table.objects.get(teams=team)
#         league = League.objects.get(table=table)
#         manager.career.get_or_create(level=league.level)
#         manager.career.total_point += team.points
#         manager.career.total_score += team.score
#         manager.career.total_win += team.wins
#         manager.career.total_draw += team.draws
#         manager.career.total_loss += team.losses
#         if team.rank == 1:
#             manager.career.total_champion += 1
#         elif team.rank == 2:
#             manager.career.total_runnerup += 1
            