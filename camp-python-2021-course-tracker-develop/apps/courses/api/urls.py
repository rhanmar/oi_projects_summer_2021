from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register(
    r"topics",
    viewsets.TopicViewSet,
    basename="topics"
)
router.register(
    r"evaluations",
    viewsets.EvaluationViewSet,
    basename="evaluations"
)
router.register(
    r"solutions",
    viewsets.SolutionViewSet,
    basename="solutions"
)

urlpatterns = router.urls
