from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from watson import search as watson


class UsersAppConfig(AppConfig):
    """Default configuration for Users app."""
    name = "apps.users"
    verbose_name = _("Users")

    def ready(self):
        # pylint: disable=unused-import,invalid-name
        from .api.auth import scheme  # noqa
        from .signals import check_avatar, copy_default_avatar_to_media  # noqa
        User = self.get_model("User")
        watson.register(
            User,
            fields=("first_name", "last_name", "email"),
        )
