from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.users.models import User


class DialogMember(BaseModel):
    """Users who are in the dialogs."""
    dialog = models.ForeignKey(
        "Dialog",
        verbose_name=_("Dialog"),
        on_delete=models.CASCADE,
        related_name="dialog_members",
    )
    member = models.ForeignKey(
        User,
        verbose_name=_("Member"),
        on_delete=models.CASCADE,
        related_name="dialog_membership",
    )

    class Meta:
        verbose_name = _("Dialog member")
        verbose_name_plural = _("Dialog members")

    def __str__(self):
        return (
            f"Dialog: {self.dialog}, "
            f"Member: {self.member.email}"
        )
