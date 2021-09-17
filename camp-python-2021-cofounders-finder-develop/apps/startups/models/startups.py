from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField

from apps.core.models import BaseModel
from apps.startups.querysets import StartupCustomQuerySet

from ..statuses import StartupChoices


class Startup(BaseModel):
    """Startup model.

    Startup is one of the main models. It is connected with
    Vacancy.

    Model is linked with User (o2m) as owner, Vacancy (o2m) and
    Comments (o2m).
    """

    status = models.CharField(
        max_length=64,
        verbose_name=_("Status"),
        choices=StartupChoices.choices,
        default=StartupChoices.STATUS_OPEN,
        help_text=_("Startup status: open, in progress, "
                    "finished, closed, archived"),
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=64,
        help_text=_("Startup Title"),
        unique=True,
    )
    slug = AutoSlugField(
        populate_from=["title"],
        blank=False,
        null=False,
    )
    text = models.TextField(
        verbose_name=_("Text"),
        max_length=2048,
        help_text=_("Info about startup"),
        blank=True,
        null=True
    )
    start_date = models.DateTimeField(
        verbose_name=_("Start Date"),
        auto_now_add=True,
        help_text=_("Date when startup starts"),
    )
    end_date = models.DateTimeField(
        verbose_name=_("End Date"),
        help_text=_("Date when startup ends"),
        validators=[MinValueValidator(timezone.now)]
    )
    owner = models.ForeignKey(
        to="users.User",
        related_name="startups",
        on_delete=models.CASCADE,
        verbose_name=_("Owner"),
        help_text=_("Startup's owner. Can be NULL if aggregated from "
                    "other service."),
        null=True,
        blank=True,
    )
    update_status_task = models.OneToOneField(
        to="django_celery_beat.PeriodicTask",
        verbose_name=_("Celery task for closing startup"),
        help_text=_("Celery task of updating status to closed"),
        null=True,
        blank=True,
        related_name="startup",
        on_delete=models.SET_NULL
    )

    objects = StartupCustomQuerySet.as_manager()

    def get_absolute_url(self) -> str:
        """Return absolute url to startup detail view."""
        return reverse("startups:startup_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        """Return startup title."""
        return self.title
