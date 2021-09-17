from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ViewSetMixin

from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.generics import HaystackGenericAPIView

from apps.startups import models as startup_models
from apps.users import models as user_models

from . import serializers


class SearchAutocompleteViewSet(
        ListModelMixin,
        ViewSetMixin,
        HaystackGenericAPIView,
):
    """Autocomplete in searching input of navbar.

    Return autocomplete title variations of: CV, Startup, Vacancy.
    """

    index_models = (
        startup_models.Startup,
        startup_models.Vacancy,
        user_models.CV,
    )
    serializer_class = serializers.SearchAutocompleteSerializer
    filter_backends = (HaystackAutocompleteFilter,)
