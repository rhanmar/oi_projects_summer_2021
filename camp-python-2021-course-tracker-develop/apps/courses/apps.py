from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoursesAppConfig(AppConfig):
    """Default configuration for Courses app."""

    name = "apps.courses"
    verbose_name = _("Courses")

    def ready(self):
        # pylint: disable=unused-import
        # import this it is required for correct work of signals
        from .signals import notify_user_about_new_evaluation  # noqa
