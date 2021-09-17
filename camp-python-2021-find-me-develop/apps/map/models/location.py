from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.map.constants import PointTypeChoices
from apps.map.querysets import LocationQuerySet


class Location(BaseModel):
    """Point on the map."""

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
    )
    point = models.PointField(
        verbose_name=_("Map point"),
    )
    point_type = models.CharField(
        verbose_name=_("Point type"),
        max_length=16,
        choices=PointTypeChoices.choices,
        default=PointTypeChoices.MEETING_POINT,
    )

    objects = LocationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return f"{self.title}: {self.point}"
