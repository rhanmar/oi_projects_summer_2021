from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, ContentTypeModel


class Attachment(BaseModel, ContentTypeModel):
    """Represent file attachments.

    Use ContentType fields and can be related to other models,
    which are defined in `allowed_models`.
    """

    related_name = "attachments"
    allowed_models = (
        "users.User",
        "courses.Course",
        "courses.Chapter",
        "courses.Topic",
        "courses.Task",
        "courses.Comment",
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        blank=True,
    )
    file = models.FileField(
        verbose_name=_("File"),
        upload_to="solutions/files/"
    )

    def __set_title(self):
        """Set file name to title if title was not given."""
        if not self.title:
            self.title = self.file.name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.__set_title()
        super().save(*args, **kwargs)

    class Meta:
        permissions = (
            ("can_change_others", _("Can change other users attachments.")),
            ("can_delete_others", _("Can delete other users attachments.")),
        )
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
