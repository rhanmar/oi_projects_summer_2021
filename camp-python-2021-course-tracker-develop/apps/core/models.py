from typing import Tuple

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from ordered_model.models import OrderedModel

from .querysets import IsHiddenFilteringOrderedQuerySet


class BaseModel(models.Model):
    """Base model for apps' models.

    This class adds to models created_at and modified_at fields.
    """

    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        verbose_name=_("modified at"),
        auto_now=True
    )

    class Meta:
        get_latest_by = "modified_at"
        abstract = True


class ContentTypeModel(models.Model):
    """Base model for contenttypes oriented models.

    This class adds to models:
    `content_type`, `object_id`, `content_object` fields.

    Params:
    `allowed_models` (tuple): Contains list of models, which can be related to
        sub model through `content_type`. For example: "users.User".
    `related_name` (str): Name to use for the relation from the related object
        back to this one.
    """

    allowed_models: Tuple[str] = ()
    related_name: str = None

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name=related_name,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    def get_model_name(self) -> str:
        """Return full name of `self.content_type` model as `<str>`."""
        model_name = self.content_type.model.capitalize()
        return f"{self.content_type.app_label}.{model_name}"

    def clean(self):
        """Raise exception if `content_type` not in `allowed_models`."""
        model_name = self.get_model_name()
        if model_name not in self.allowed_models:
            raise ValidationError(
                f"{self.content_type} is not in {self.allowed_models} field."
            )

    class Meta:
        abstract = True


class BaseDurationModel(models.Model):
    """Base model that adds `start_date` and `finish_date` fields."""

    start_date = models.DateField(
        verbose_name=_("Start date"),
    )
    finish_date = models.DateField(
        verbose_name=_("Finish date"),
    )

    def clean(self):
        """Validate model fields."""
        if self.finish_date < self.start_date:
            raise ValidationError({
                "finish_date": "Finish date must be greater or equal "
                               "than start date.",
            })

    class Meta:
        abstract = True


class BaseOrderedModel(OrderedModel):
    """Abstract model that allows objects to be ordered relative to each other.
    Provides an ``order`` field.

    Use custom QuerySet `IsHiddenFilteringOrderedQuerySet`.
    """

    objects = models.Manager.from_queryset(
        IsHiddenFilteringOrderedQuerySet
    )()

    class Meta:
        abstract = True
