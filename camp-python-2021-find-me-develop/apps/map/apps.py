from django.apps import AppConfig

from watson import search as watson


class MapConfig(AppConfig):
    """default configuration for Map app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.map"

    def ready(self):
        # pylint: disable=unused-import,invalid-name
        Meeting = self.get_model("Meeting")
        watson.register(Meeting, fields=("title", "description"))
