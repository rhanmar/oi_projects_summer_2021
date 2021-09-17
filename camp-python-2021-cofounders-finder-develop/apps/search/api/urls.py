from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register(
    r"search-autocomplete",
    viewsets.SearchAutocompleteViewSet,
    basename="search-autocomplete"
)
urlpatterns = router.urls
