from django.contrib import admin

from .models import Location, Meeting, MeetingReview


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """UI for Location model."""


@admin.register(Meeting)
class MeetingPointAdmin(admin.ModelAdmin):
    """UI for Meeting model."""


@admin.register(MeetingReview)
class MeetingReviewAdmin(admin.ModelAdmin):
    """UI for MeetingReview model."""
