from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.models.users import User

from ..statuses import RequestChoices


class Request(BaseModel):
    """Request model.

    When user wants to join to the startup, he makes Request to the desired
    vacancy.
    Request can be under consideration, rejected or archived.
    Request is linked with Vacancy (o2m) and User (o2m).

    """
    vacancy = models.ForeignKey(
        to="startups.Vacancy",
        related_name="requests",
        on_delete=models.DO_NOTHING,
        verbose_name=_("Vacancy"),
        help_text=_("Request's vacancy"),
    )

    status = models.CharField(
        max_length=64,
        verbose_name=_("Status"),
        choices=RequestChoices.choices,
        default=RequestChoices.STATUS_UNDER_CONSIDERATION,
        help_text=_("Request status: under consideration, rejected, archived"),
    )
    message = models.TextField(
        verbose_name=_("Message"),
        help_text=_("Request message"),
    )
    user = models.ForeignKey(
        to=User,
        related_name="requests",
        on_delete=models.DO_NOTHING,
        verbose_name=_("User"),
        help_text=_("Request's User"),
    )

    def __str__(self) -> str:
        """Return Request info."""
        return (f"Request by {self.user.first_name} {self.user.last_name}"
                f" on {self.vacancy.title}")

    class Meta:
        unique_together = ("user", "vacancy",)

    def clean(self):
        """Check if user already sent request to vacancy."""
        self.validate_unique()
        super().clean()
