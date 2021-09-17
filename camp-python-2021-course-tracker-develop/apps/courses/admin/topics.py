from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from .. import models
from .attachments import AttachmentInline
from .tasks import TaskInline


@admin.register(models.Topic)
class TopicAdmin(OrderedModelAdmin):
    """Represent Admin interface for model Topic."""

    list_display = (
        "chapter",
        "speaker",
        "title",
        "order",
        "created_at",
        "modified_at",
        "move_up_down_links",
        "reading_date"
    )
    fields = (
        "chapter",
        "speaker",
        "title",
        "description",
        "order",
        "created_at",
        "modified_at",
        "tags",
    )
    filter_horizontal = (
        "tags",
    )
    list_filter = (
        "created_at",
        "modified_at"
    )
    readonly_fields = (
        "order",
        "move_up_down_links",
        "created_at",
        "modified_at",
    )
    search_fields = (
        "title",
        "description"
    )
    ordering = (
        "order",
    )

    inlines = (
        TaskInline,
        AttachmentInline,
    )
