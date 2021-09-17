from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class Dialog(BaseModel):
    """Model for dialog between two users."""
    user1 = models.ForeignKey(
        to="users.User",
        related_name="dialogs_of_user1",
        on_delete=models.CASCADE,
        verbose_name=_("User1"),
    )
    user2 = models.ForeignKey(
        to="users.User",
        related_name="dialogs_of_user2",
        on_delete=models.CASCADE,
        verbose_name=_("User2"),
    )

    class Meta:
        unique_together = ("user1", "user2")
        verbose_name = _("Dialog")
        verbose_name_plural = _("Dialogs")

    def __str__(self):
        return f"Dialog between {self.user1.email} to {self.user2.email}"

    @staticmethod
    def dialog_exists(user1, user2):
        """Check if dialog between two users exists."""
        # TODO: Write a custom queryset (or a manager)
        return Dialog.objects.filter(
            Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)
        ).exists()

    @staticmethod
    def create_if_not_exists(user1, user2):
        """Create new dialog if dialog not exists."""
        dialog_exists = Dialog.dialog_exists(user1, user2)
        if not dialog_exists:
            Dialog.objects.create(user1=user1, user2=user2)

    @staticmethod
    def get_dialogs_for_user(user):
        """Get all dialogs for user."""
        return Dialog.objects.filter(
            Q(user1=user) | Q(user2=user)
        )


class Message(BaseModel):
    """Model for text message."""
    sender = models.ForeignKey(
        to="users.User",
        related_name="from_user",
        on_delete=models.CASCADE,
        verbose_name=_("Sender"),
    )
    recipient = models.ForeignKey(
        to="users.User",
        related_name="to_user",
        on_delete=models.CASCADE,
        verbose_name=_("Recipient"),
    )
    text = models.TextField(
        verbose_name=_("Text"),
        blank=True
    )

    @staticmethod
    def get_messages_for_dialog(sender, recipient):
        """Get last messages for dialog between sender and recipient."""
        return Message.objects.filter(
            Q(sender_id=sender, recipient_id=recipient) |
            Q(sender_id=recipient, recipient_id=sender)
        )

    def __str__(self):
        return f"Message from {self.sender.email} to {self.recipient.email}"

    def save(self, **kwargs):
        """Save message and create new dialog if it not exists."""
        super().save(**kwargs)
        Dialog.create_if_not_exists(self.sender, self.recipient)

    class Meta:
        ordering = ("-created",)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
