from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from apps.core.models import BaseModel, ContentTypeModel
from apps.courses.querysets import CommentQuerySet


class Comment(BaseModel, ContentTypeModel):
    """Represent user`s comment.

    Use ContentType fields and can be related to other models,
    which are defined in `allowed_models`.
    """

    related_name = "comments"
    allowed_models = (
        "users.User",
        "courses.Course",
        "courses.Chapter",
        "courses.Topic",
        "courses.Task",
        "courses.Comment",
    )

    user = models.ForeignKey(
        verbose_name=_("User"),
        to="users.User",
        on_delete=models.CASCADE,
    )
    parent = models.ForeignKey(
        verbose_name=_("Parent"),
        to="courses.Comment",
        on_delete=models.CASCADE,
        related_name="sub_comments",
        null=True,
        blank=True
    )
    text = RichTextField(
        verbose_name=_("Text"),
        max_length=6800,
        config_name="text_only"
    )

    objects = CommentQuerySet.as_manager()

    class Meta:
        permissions = (
            ("can_change_others", _("Can change other users attachments.")),
            ("can_delete_others", _("Can delete other users attachments.")),
        )
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
