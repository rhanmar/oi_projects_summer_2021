from django.contrib import admin

from apps.courses.models.tags import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Represent admin dashboard for model Tag."""

    list_display = (
        "name",
    )
    search_fields = (
        "name",
    )
