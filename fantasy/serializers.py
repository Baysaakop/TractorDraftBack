from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Career, Manager, Match, Gameweek, TableTeam, Table, League, Duel, League19, League19Team

class CareerSerializer(serializers.ModelSerializer):     
    class Meta:
        model = Career
        fields = (            
            'id', 'level', 'total_champion', 'total_runnerup', 'total_third', 'total_point', 'total_win', 'total_draw', 'total_loss', 'total_score', 'total_score_away', 'total_appearance', 'total_topscorer', 'total_topscorer_away', 'total_vanga'
        )        

class ManagerSerializer(serializers.ModelSerializer): 
    image = serializers.ImageField(required=False, use_url=True)
    career = CareerSerializer(many=True)
    class Meta:
        model = Manager
        fields = (
            'id', 'name', 'description', 'career', 'image', 'created_by', 'updated_by', 'created_at', 'updated_at'            
        )        

class MatchSerializer(serializers.ModelSerializer):    
    home_team = ManagerSerializer(read_only=True)
    away_team = ManagerSerializer(read_only=True)
    class Meta:
        model = Match
        fields = (
            'id', 'created_by', 'updated_by', 'created_at', 'updated_at',
            'home_team', 'away_team', 'home_score', 'away_score'
        )     

class GameweekSerializer(serializers.ModelSerializer): 
    token = serializers.CharField(write_only=True) 
    matches = MatchSerializer(many=True, read_only=True)
    class Meta:
        model = Gameweek
        fields = (
            'id', 'name', 'week', 'matches', 'token'          
        )  

class TableTeamSerializer(serializers.ModelSerializer):   
    manager = ManagerSerializer() 
    manager_name = serializers.SerializerMethodField('get_manager_name')   
    class Meta:
        model = TableTeam
        fields = (
            'id', 'name', 'manager', 'manager_name', 'rank', 'created_by', 'updated_by', 'created_at', 'updated_at',
            'wins', 'draws', 'losses', 'score', 'score_away', 'points', 'topscorer', 'topscorer_away', 'vanga'
        )  

    def get_manager_name(self, obj):
        return obj.manager.name

class TableSerializer(serializers.ModelSerializer):    
    teams = TableTeamSerializer(many=True) 
    class Meta:
        model = Table
        fields = (
            'id', 'name', 'teams', 'created_by', 'updated_by', 'created_at', 'updated_at'            
        )      

class LeagueSerializer(serializers.ModelSerializer):    
    # token = serializers.CharField(write_only=True)
    table = TableSerializer()
    gameweeks = GameweekSerializer(many=True)         
    class Meta:
        model = League
        fields = (
            'id', 'name', 'year', 'number', 'level', 'description', 'isFinished', 'table', 'gameweeks', 'created_by', 'updated_by', 'created_at', 'updated_at'         
        )      

class DuelSerializer(serializers.ModelSerializer):     
    team1 = ManagerSerializer() 
    team2 = ManagerSerializer() 
    class Meta:
        model = Duel
        fields = (            
            'team1', 'team2', 'win1', 'win2', 'draw'
        )  

class League19TeamSerializer(serializers.ModelSerializer):     
    manager = ManagerSerializer() 
    class Meta:
        model = League19Team
        fields = (            
            'name', 'manager', 'wins', 'draws', 'losses', 'score', 'points', 'league1', 'league2', 'league3', 'league4'
        )  

class League19Serializer(serializers.ModelSerializer):        
    teams = League19TeamSerializer(many=True, read_only=True)         
    class Meta:
        model = League19
        fields = (
            'id', 'teams', 'created_by', 'updated_by', 'created_at', 'updated_at'            
        ) 