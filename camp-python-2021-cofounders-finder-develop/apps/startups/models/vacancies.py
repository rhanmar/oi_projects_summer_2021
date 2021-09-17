from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from ..statuses import VacancyChoices


class Vacancy(BaseModel):
    """Vacancy model.

    This model contains info about vacancy. Every vacancy belongs to
    the startup.
    It is connected with Requests and Employees.
    Can be open, closed or archived.

    """
    status = models.CharField(
        max_length=64,
        verbose_name=_("Status"),
        choices=VacancyChoices.choices,
        default=VacancyChoices.STATUS_OPEN,
        help_text=_("Vacancy status: open, closed, archived"),
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
        help_text=_("Vacancy Title"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Info about vacancy"),
    )
    startup = models.ForeignKey(
        to="startups.Startup",
        related_name="vacancies",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Startup"),
        help_text=_("Vacancy's startup"),
    )
    skills = models.ManyToManyField(
        to="skills.Skill",
        verbose_name=_("Skill"),
        help_text=_(
            "Required skills for this vacancy."
        ),
    )
    url = models.URLField(
        verbose_name=_("URL"),
        help_text=_("Can be set if vacancy aggregated from other service."),
        null=True,
        blank=True,
    )

    def get_absolute_url(self) -> str:
        """Return absolute url to Vacancy detail view."""
        return reverse("startups:vacancy_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        """Return vacancy title."""
        return self.title

    def requests_users(self):
        """Return array of users which requests on self vacancy."""
        requests_users = []
        for request in self.requests.select_related("user"):
            requests_users.append(request.user)
        return requests_users
