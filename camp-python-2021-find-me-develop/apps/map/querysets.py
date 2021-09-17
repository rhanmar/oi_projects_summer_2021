from django.db import models
from django.db.models import Q
from django.utils import timezone

from .constants import PointTypeChoices


class LocationQuerySet(models.QuerySet):
    """Custom queryset for Location model."""

    def meeting_points(self):
        """Return queryset consists only meeting points locations."""
        return self.filter(
            Q(point_type=PointTypeChoices.MEETING_POINT) &
            Q(meeting__deadline__gte=timezone.now())
        )

    def user_points(self):
        """Return queryset consists only user points locations."""
        return self.filter(point_type=PointTypeChoices.USER_POINT)

    def fresh_all_locations(self):
        """Return queryset consists only fresh meetings or user locations."""
        return self.filter(
            Q(point_type=PointTypeChoices.MEETING_POINT) &
            Q(meeting__deadline__gte=timezone.now()) |
            Q(point_type=PointTypeChoices.USER_POINT)
        )


class MeetingQuerySet(models.QuerySet):
    """Custom queryset for Meeting model."""

    def active_meetings(self):
        """Return queryset with active meetings."""
        return self.filter(deadline__gte=timezone.now())
