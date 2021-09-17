from django.contrib import admin

from apps.comments.models import Comment
from apps.core.admin import BaseAdmin


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    """UI for Comment model."""

    list_display = (
        "title",
        "text",
        "author",
        "parent_comment",
    )

    list_select_related = (
        "author",
        "parent_comment",
    )

    ordering = (
        "author",
        "parent_comment",
    )

    list_filter = (
        "author",
        "parent_comment",
    )
