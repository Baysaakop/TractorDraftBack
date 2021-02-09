from django.db import models
from django.contrib.auth.models import User

def item_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/items/<id>/<filename> 
    return 'items/{0}/{1}'.format(instance.id, filename) 

class Career(models.Model):
    level = models.IntegerField(default=1)
    total_champion = models.IntegerField(default=0)
    total_runnerup = models.IntegerField(default=0)
    total_third = models.IntegerField(default=0)
    total_point = models.IntegerField(default=0)    
    total_win = models.IntegerField(default=0)
    total_draw = models.IntegerField(default=0)
    total_loss = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    total_score_away = models.IntegerField(default=0)
    total_appearance = models.IntegerField(default=0)
    total_match = models.IntegerField(default=0)
    total_topscorer = models.IntegerField(default=0)
    total_topscorer_away = models.IntegerField(default=0)
    total_vanga = models.IntegerField(default=0)

class Manager(models.Model):
    name = models.CharField(max_length=50)    
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=item_directory_path, null=True, blank=True)
    career = models.ManyToManyField(Career, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="manager_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="manager_updated_by")

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name="home_team")    
    away_team = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name="away_team")    
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="match_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="match_updated_by") 

class Gameweek(models.Model):
    name = models.CharField(max_length=50)    
    week = models.IntegerField(default=0)    
    matches = models.ManyToManyField(Match, null=True, blank=True)                  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="gameweek_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="gameweek_updated_by")

    def __str__(self):
        return self.name  

class TableTeam(models.Model):
    name = models.CharField(max_length=50)    
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)        
    draws = models.IntegerField(default=0)   
    losses = models.IntegerField(default=0)    
    points = models.IntegerField(default=0)            
    score = models.IntegerField(default=0)
    score_away = models.IntegerField(default=0)   
    topscorer = models.IntegerField(default=0) 
    topscorer_away = models.IntegerField(default=0) 
    vanga = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="tableteam_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="tableteam_updated_by")

    def __str__(self):
        return self.name  

class Table(models.Model):
    name = models.CharField(max_length=50)    
    teams = models.ManyToManyField(TableTeam, null=True, blank=True)                     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="table_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="table_updated_by")

    def __str__(self):
        return self.name  

class League(models.Model):
    name = models.CharField(max_length=50)    
    year = models.IntegerField(default=0)  
    number = models.IntegerField(default=0)    
    level = models.IntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    isFinished = models.BooleanField(default=False)
    image = models.ImageField(upload_to=item_directory_path, null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)    
    gameweeks = models.ManyToManyField(Gameweek, null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="league_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="league_updated_by")

    def __str__(self):
        return self.name

class Duel(models.Model):
    team1 = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name="team2")
    win1 = models.IntegerField(default=0)
    win2 = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)

    def __str__(self):
        return self.team1.name + "-" + self.team2.name

class League19Team(models.Model):
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    league1 = models.IntegerField(default=0)
    league2 = models.IntegerField(default=0)
    league3 = models.IntegerField(default=0)
    league4 = models.IntegerField(default=0)

class League19(models.Model):
    name = models.CharField(max_length=50)    
    teams = models.ManyToManyField(League19Team)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="league19_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="league19_updated_by")

    def __str__(self):
        return self.name
    
