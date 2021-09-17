from django.contrib import admin

from apps.courses.models.comments import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Represent Admin interface for model Comment with contenttypes fields."""

    list_display = (
        "user",
        "created_at",
        "modified_at"
    )
    list_filter = (
        "created_at",
        "modified_at"
    )
