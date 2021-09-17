from django.db.models import QuerySet


class UserQuerySet(QuerySet):
    """Custom queryset for User model."""

    def mentors(self):
        """Return all courses mentors."""
        return self.filter(groups__name="Mentor")

    def students(self):
        """Return all courses students."""
        return self.filter(groups__name="Student")
