from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel, ContentTypeModel


class Rating(BaseModel, ContentTypeModel):
    """Represent user`s rating.

    Uses ContentType fields and can be related to other models,
    which are defined in `allowed_models`.
    """

    related_name = "ratings"
    allowed_models = ()

    user = models.ForeignKey(
        verbose_name=_("User"),
        to="users.User",
        on_delete=models.CASCADE
    )
    mark = models.PositiveSmallIntegerField(
        verbose_name=_("Mark"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        unique_together = [
            ["content_type", "object_id", "user"]
        ]
