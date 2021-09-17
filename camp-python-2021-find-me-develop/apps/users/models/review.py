from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Review(BaseModel):
    """Review from other users to the user."""

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
    )
    body = models.TextField(
        verbose_name=_("Body"),
        blank=True,
    )
    rate = models.FloatField(
        verbose_name=_("Rate"),
        default=5.0,
    )
    reviewer = models.ForeignKey(
        "User",
        verbose_name=_("Sender"),
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    reviewed = models.ForeignKey(
        "User",
        verbose_name=_("Recipient"),
        related_name="reviews_of",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        unique_together = ["reviewer", "reviewed"]

    def __str__(self):
        # pylint: disable=no-member
        reviewer_name = self.reviewer.get_fullname()
        reviewed_name = self.reviewed.get_fullname()
        return f"{reviewer_name}: {self.title} to {reviewed_name}"
