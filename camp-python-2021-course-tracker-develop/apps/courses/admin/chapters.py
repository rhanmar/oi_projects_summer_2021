from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from .. import models
from .attachments import AttachmentInline


class TopicInline(admin.TabularInline):
    """InLine for Topic."""

    model = models.Topic


@admin.register(models.Chapter)
class ChapterAdmin(OrderedModelAdmin):
    """Represent Admin interface for model Chapter."""

    list_display = (
        "course",
        "title",
        "is_hidden",
        "order",
        "start_date",
        "finish_date",
        "created_at",
        "modified_at",
        "move_up_down_links"
    )
    list_filter = (
        "is_hidden",
        "start_date",
        "finish_date",
        "created_at",
        "modified_at"
    )
    fields = (
        "course",
        "title",
        "description",
        "is_hidden",
        "order",
        "start_date",
        "finish_date",
        "created_at",
        "modified_at",
        "move_up_down_links"
    )
    search_fields = (
        "title",
        "description"
    )
    readonly_fields = (
        "move_up_down_links",
        "order",
        "created_at",
        "modified_at"
    )
    ordering = (
        "order",
    )

    inlines = (
        TopicInline,
        AttachmentInline,
    )
