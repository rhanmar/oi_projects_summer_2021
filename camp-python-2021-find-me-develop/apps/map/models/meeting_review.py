from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class MeetingReview(BaseModel):
    """Review about Meeting point."""

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
    )
    body = models.TextField(
        verbose_name=_("Body review"),
        blank=True,
    )
    rate = models.FloatField(
        verbose_name=_("Rate"),
        default=5.0,
    )
    created_by = models.ForeignKey(
        "users.User",
        verbose_name=_("Created by"),
        on_delete=models.CASCADE,
    )
    meeting = models.ForeignKey(
        "Meeting",
        verbose_name=_("Meeting point"),
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    class Meta:
        verbose_name = _("Meeting review")
        verbose_name_plural = _("Meeting reviews")
        unique_together = ("meeting", "created_by")

    def __str__(self):
        # pylint: disable=no-member
        sender_name = self.created_by.get_fullname()
        meeting_title = self.meeting.title
        return f"{meeting_title}: {self.title} by {sender_name}"
