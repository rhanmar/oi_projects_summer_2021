from django.db.models import QuerySet

from .statuses import StartupChoices


class StartupCustomQuerySet(QuerySet):
    """Custom QuerySet which add .active() method."""

    def active(self):
        """Return QuerySet of Startups that statuses
        either: `open` or `in progress`.
        """
        return self.filter(
            status__in=[
                StartupChoices.STATUS_OPEN,
                StartupChoices.STATUS_IN_PROGRESS,
            ]
        )
