from drf_haystack.serializers import HaystackSerializer

from apps.search import search_indexes


class SearchAutocompleteSerializer(HaystackSerializer):
    """Autocomplete in searching input of navbar.

    Autocomplete titles of models: CV, Startup, Vacancy.
    """

    class Meta:
        index_classes = (
            search_indexes.CVIndex,
            search_indexes.StartupIndex,
            search_indexes.VacancyIndex,
        )
        fields = (
            "autocomplete",
        )

        # The `field_aliases` attribute can be used in order to alias a
        # query parameter to a field attribute. In this case a query like
        # /search/?q=Vue would alias the `q` parameter to the `autocomplete`
        # field on the index.
        field_aliases = {
            "q": "autocomplete",
        }

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError
