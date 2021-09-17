from django.contrib.postgres.fields.citext import CICharField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    """Represent tag for Topic."""

    name = CICharField(
        verbose_name=_("Name"),
        max_length=35,
        unique=True
    )

    def __str__(self):
        # pylint: disable=invalid-str-returned
        return self.name
