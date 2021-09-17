from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .. import models


class AttachmentInline(GenericTabularInline):
    """InLine for attachment(ContentType)."""

    model = models.Attachment


@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """Represent admin model for model Attachment with contenttypes fields."""

    list_display = (
        "title",
        "file",
        "content_type",
        "object_id",
        "content_object"
    )
    list_filter = (
        "created_at",
        "modified_at"
    )
