from django.apps import AppConfig


class CommentsConfig(AppConfig):
    """Config for Comment models."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.comments"
