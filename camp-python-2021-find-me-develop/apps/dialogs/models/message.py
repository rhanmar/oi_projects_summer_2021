from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.models import User


class Message(BaseModel):
    """Messages exchanged by users."""
    text = models.TextField(
        verbose_name=_("Text message"),
    )
    sender = models.ForeignKey(
        User,
        verbose_name=_("Sender"),
        on_delete=models.CASCADE,
    )
    dialog = models.ForeignKey(
        "Dialog",
        verbose_name=_("Dialog"),
        on_delete=models.CASCADE,
        related_name="messages",
    )

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return (
            f"Sender: {self.sender.email}, "
            f"Dialog: {self.dialog}"
        )
