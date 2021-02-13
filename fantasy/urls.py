from .views import ManagerViewSet, MatchViewSet, GameweekViewSet, TableTeamViewSet, TableViewSet, LeagueViewSet, DuelViewSet, League19TeamViewSet, League19ViewSet, PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'managers', ManagerViewSet, basename='managers')
router.register(r'matches', MatchViewSet, basename='matches')
router.register(r'gameweeks', GameweekViewSet, basename='gameweeks')
router.register(r'tableteams', TableTeamViewSet, basename='tableteams')
router.register(r'tables', TableViewSet, basename='tables')
router.register(r'leagues', LeagueViewSet, basename='leagues')
router.register(r'duels', DuelViewSet, basename='duels')
router.register(r'league19teams', League19TeamViewSet, basename='league19teams')
router.register(r'league19', League19ViewSet, basename='league19')
router.register(r'posts', PostViewSet, basename='posts')
urlpatterns = router.urls