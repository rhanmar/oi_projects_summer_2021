from django.contrib import admin

from apps.courses.models.ratings import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Represent Admin interface for model Rating."""

    list_display = (
        "user",
        "content_type",
        "mark",
        "created_at",
        "modified_at"
    )
    list_filter = (
        "mark",
        "content_type"
    )
