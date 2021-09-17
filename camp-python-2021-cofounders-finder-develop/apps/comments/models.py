from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel
from apps.startups.models import Startup
from apps.users.models.users import User


class Comment(BaseModel):
    """Model stores comments.

    This model stores a comment information, author of it, post (startup) and
    parent comment.

    Comment is linked with User (o2m) as author, Startup (o2m)
    and itself (o2m).

    """

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
    )

    text = models.TextField(
        verbose_name=_("Comment text"),
        blank=True,
    )

    author = models.ForeignKey(
        to=User,
        related_name="comments",
        verbose_name=_("Author"),
        on_delete=models.CASCADE,
        help_text=_(
            "Indicates the author of the comment.",
        ),
    )

    parent_comment = models.ForeignKey(
        verbose_name=_("Parent of comment"),
        related_name="comments",
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        help_text=_(
            "Allows to create a tree-like structure of comments.",
        ),
    )

    startup = models.ForeignKey(
        to=Startup,
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name=_("Startup"),
        help_text=_("Comment about Startup"),
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def clean(self):
        """Check if startups of parent and created comments are equal."""
        if self.parent_comment and self.startup != self.parent_comment.startup:
            raise ValidationError(
                {
                    "parent_comment": _(
                        "The parent comment refers to another startup."
                    ),
                }
            )
        super().clean()
