from django.db.models import Avg, QuerySet

from apps.users.constants import NUMBER_OF_TOP


class UserQuerySet(QuerySet):
    """QuerySet for model User."""

    def with_rating(self):
        """Get users and their average rating."""
        return self.annotate(rating=Avg("reviews_of__rate"))

    def get_top_users(self, number_of_top=NUMBER_OF_TOP):
        """Get top users with max rating."""
        return self.with_rating() \
                   .order_by("-rating") \
                   .filter(rating__isnull=False)[:number_of_top]
