from django.contrib import admin

from .. import models
from .attachments import AttachmentInline


class ChapterInline(admin.TabularInline):
    """InLine for Chapter."""

    model = models.Chapter


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    """Represent Admin interface for model Course."""

    list_display = (
        "title",
        "is_hidden",
        "start_date",
        "finish_date",
        "created_at"
    )
    filter_horizontal = (
        "users",
    )
    list_filter = (
        "is_hidden",
        "start_date",
        "finish_date",
        "created_at",
        "modified_at"
    )
    search_fields = (
        "title",
        "description"
    )

    inlines = (
        ChapterInline,
        AttachmentInline,
    )
