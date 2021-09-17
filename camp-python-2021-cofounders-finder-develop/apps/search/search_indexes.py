from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from apps.startups import models as startups_models
from apps.users import models as users_models


class CVIndex(CelerySearchIndex, indexes.Indexable):
    """Haystack searching index for CV model."""

    text = indexes.CharField(document=True, use_template=True)
    autocomplete = indexes.EdgeNgramField(model_attr="title")

    def get_model(self):
        """Return CV model."""
        return users_models.CV


class StartupIndex(CelerySearchIndex, indexes.Indexable):
    """Haystack searching index for Startup model."""

    text = indexes.CharField(document=True, use_template=True)
    autocomplete = indexes.EdgeNgramField(model_attr="title")

    def get_model(self):
        """Return Startup model."""
        return startups_models.Startup


class VacancyIndex(CelerySearchIndex, indexes.Indexable):
    """Haystack searching index for Vacancy model."""

    text = indexes.CharField(document=True, use_template=True)
    autocomplete = indexes.EdgeNgramField(model_attr="title")

    def get_model(self):
        """Return Vacancy model."""
        return startups_models.Vacancy
