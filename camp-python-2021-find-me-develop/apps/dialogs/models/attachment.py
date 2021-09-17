from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Attachment(BaseModel):
    """File attachment in message."""
    file = models.FileField(
        verbose_name=_("File"),
        upload_to=settings.DEFAULT_MEDIA_PATH,
        max_length=255,
    )
    message = models.ForeignKey(
        "Message",
        verbose_name=_("Message"),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")

    def __str__(self):
        return f"File name: { self.file.name }"
