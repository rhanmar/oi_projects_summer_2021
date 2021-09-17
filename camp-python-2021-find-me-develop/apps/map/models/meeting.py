from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit import models as imagekitmodels
from imagekit.processors import Transpose

from apps.core.models import BaseModel
from apps.map.querysets import MeetingQuerySet


def get_default_deadline():
    """Return default value for meeting deadline greater now to one hour."""
    return datetime.now() + timedelta(hours=1)


class Meeting(BaseModel):
    """Leave point on the map about meeting."""

    title = models.CharField(
        verbose_name=_("Point name"),
        max_length=100,
    )
    description = models.TextField(
        verbose_name=_("Meeting description"),
        blank=True,
    )
    max_people_limit = models.IntegerField(
        verbose_name=_("Max people in one meeting"),
        default=1,
    )
    photo = imagekitmodels.ProcessedImageField(
        verbose_name=_("Avatar"),
        blank=True,
        null=True,
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=512,
        processors=[Transpose()],
        options={
            "quality": 100,
        }
    )
    deadline = models.DateTimeField(
        verbose_name=_("Delete time"),
        default=get_default_deadline,
    )
    created_by = models.ForeignKey(
        "users.User",
        verbose_name=_("Created by"),
        related_name="created_meetings",
        on_delete=models.CASCADE,
    )
    location = models.OneToOneField(
        "Location",
        verbose_name=_("Map location"),
        on_delete=models.CASCADE,
    )
    dialog = models.OneToOneField(
        "dialogs.Dialog",
        verbose_name=_("Dialog"),
        on_delete=models.CASCADE,
    )

    objects = MeetingQuerySet.as_manager()

    class Meta:
        verbose_name = _("Meeting")
        verbose_name_plural = _("Meetings")

    def get_absolute_url(self):
        """Return url of meeting dialog."""
        # pylint: disable=no-member
        return self.dialog.get_absolute_url()

    def __str__(self):
        # pylint: disable=no-member
        user_name = self.created_by.get_fullname()
        return f"{user_name}: {self.title}"
