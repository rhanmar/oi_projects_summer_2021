from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Skill(BaseModel):
    """Skill model.

    Filled by list of skills (fields of activity, programing
    languages, frameworks.
    Connected only with vacancy.

    """

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=64,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name
