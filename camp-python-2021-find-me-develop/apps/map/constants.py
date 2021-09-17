from django.db import models
from django.utils.translation import gettext_lazy as _


class PointTypeChoices(models.TextChoices):
    """Variants of point type."""

    USER_POINT = "UserPoint", _("UserPoint")
    MEETING_POINT = "Meeting", _("Meeting")
