from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from imagekit import models as imagekitmodels
from imagekit.processors import ResizeToFill, Transpose

from apps.core.models import BaseModel


class Dialog(BaseModel):
    """Dialog model containing title and logo."""
    title = models.TextField(
        verbose_name=_("Dialog title"),
        max_length=100,
    )
    logo = imagekitmodels.ProcessedImageField(
        verbose_name=_("Logo"),
        blank=True,
        null=True,
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=255,
        processors=[Transpose()],
        options={
            "quality": 100,
        },
    )
    logo_thumbnail = imagekitmodels.ImageSpecField(
        source="logo",
        processors=[
            ResizeToFill(50, 50)
        ],
    )

    class Meta:
        verbose_name = _("Dialog")
        verbose_name_plural = _("Dialogs")

    def get_absolute_url(self):
        """Return dialog's absolute url."""
        return reverse("dialog_detail", kwargs={"dialog_id": self.pk})

    def __str__(self):
        return self.title
