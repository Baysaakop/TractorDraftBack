from django.core.management.base import BaseCommand
from fantasy.models import Career, Manager, Match, Gameweek, TableTeam, Table, League, Duel

class Command(BaseCommand):
    def handle(self, *args, **kwargs):            
        for career in Career.objects.all():
            career.total_champion=0
            career.total_runnerup=0
            career.total_third=0
            career.save()
        for league in League.objects.all():
            for team in league.table.teams.all():           
                career = team.manager.career.filter(level=league.level)[0]                     
                if career is not None:
                    if (team.rank == 1):
                        career.total_champion+=1
                    elif (team.rank == 2):
                        career.total_runnerup+=1
                    elif (team.rank == 3):
                        career.total_third+=1
                    career.save()                        
        self.stdout.write(self.style.SUCCESS('Reset all data'))