from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class UserReport(BaseModel):
    """Bad behavior report to the user from other users."""

    reason = models.CharField(
        verbose_name=_("Report reason"),
        max_length=150,
        blank=True,
    )
    created_by = models.ForeignKey(
        "User",
        verbose_name=_("Reporter"),
        related_name="reports_from",
        on_delete=models.CASCADE,
    )
    reported = models.ForeignKey(
        "User",
        verbose_name=_("Reported user"),
        related_name="reports_to",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("User report")
        verbose_name_plural = _("User reports")
        unique_together = ["created_by", "reported"]

    def __str__(self):
        # pylint: disable=no-member
        reported_name = self.reported.get_fullname()
        created_by_name = self.created_by.get_fullname()
        return f"{reported_name} - {self.reason} by {created_by_name}"
