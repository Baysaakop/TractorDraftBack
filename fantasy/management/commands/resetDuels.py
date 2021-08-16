from django.core.management.base import BaseCommand
from fantasy.models import Career, Manager, Match, Gameweek, TableTeam, Table, League, Duel
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Duel.objects.all().delete()
        for match in Match.objects.all():
            if match.home_score > 0 and match.away_score > 0:
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
        self.stdout.write(self.style.SUCCESS('Reset all data'))
