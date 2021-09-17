from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class BlackList(BaseModel):
    """Banned users for the only one user.

    'user' filed is info about blacklist owner,
    'banned_user' field if info about added to blacklist user.

    'user' related_name means that we can get list of banned users for current
    user (or we can get user's blacklist).
    Alternative name is 'bans'.
    Example: user.banned.all() == (Blacklist.objects.filter(user_id=user.id))

    'banned_user' related_name means that we can get list of users, who banned
    current user (or list of blacklists with current user).
    Alternative name is 'who_banned_me'.
    Example: user.banned_by.all() == (Blacklist.objects.filter(
                                        banned_user_id=user.id))
    """

    user = models.ForeignKey(
        "User",
        verbose_name=_("User"),
        related_name="banned",
        on_delete=models.CASCADE,
    )
    banned_user = models.ForeignKey(
        "User",
        verbose_name=_("Banned user"),
        related_name="banned_by",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Black List member")
        verbose_name_plural = _("Black List members")
        unique_together = ["user", "banned_user"]

    def __str__(self):
        # pylint: disable=no-member
        user_name = self.user.get_fullname()
        banned_user_name = self.banned_user.get_fullname()
        return f"{user_name}: -{banned_user_name}"
