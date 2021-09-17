from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Employee(BaseModel):
    """Employee model.

    User becomes employee when he is accepted to the vacancy.
    Model is linked with Vacancy (o2m) and User (o2m).

    """
    vacancy = models.ForeignKey(
        to="startups.Vacancy",
        related_name="employees",
        on_delete=models.CASCADE,
        verbose_name=_("Vacancy"),
        help_text=_("Employee's vacancy"),
    )
    user = models.ForeignKey(
        to="users.User",
        related_name="jobs",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("Employee in the Startup is User"),
    )

    def __str__(self) -> str:
        """Return Employee info."""
        return (
            f"{self.user.first_name} {self.user.last_name} "
            f"works on {self.vacancy.title}"
        )
