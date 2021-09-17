from django.db.models import QuerySet

from ordered_model.models import OrderedModelQuerySet


class IsHiddenFilterQuerySet(QuerySet):
    """Add `not_hidden()` QuerySet method."""

    def not_hidden(self) -> QuerySet:
        """Return filtered QuerySet by `is_hidden=False`."""

        return self.filter(is_hidden=False)


class IsHiddenFilteringOrderedQuerySet(
    OrderedModelQuerySet,
    IsHiddenFilterQuerySet
):
    """Custom queryset for ordered models with boolean `is_hidden` field."""
