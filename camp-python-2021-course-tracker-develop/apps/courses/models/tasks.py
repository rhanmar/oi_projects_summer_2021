import os

from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from apps.core.models import BaseModel, BaseOrderedModel
from apps.courses.querysets import SolutionQuerySet, TaskQuerySet

from .comments import Comment


class Task(BaseModel, BaseOrderedModel):
    """Represent ORM model of task."""

    order_with_respect_to = "topic"

    topic = models.ForeignKey(
        verbose_name=_("Topic"),
        to="courses.Topic",
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,

    )
    description = RichTextField(
        verbose_name=_("Description"),
        max_length=16000,
        config_name="tasks_text",
    )

    jira_tag = models.CharField(
        verbose_name=_("Jira tag"),
        max_length=15,
        blank=True,
    )

    is_hidden = models.BooleanField(
        verbose_name=_("Is hidden"),
        default=False
    )

    solution = models.ManyToManyField(
        verbose_name=_("solution"),
        to="users.User",
        through="Solution",
    )
    comments = GenericRelation(Comment)

    objects = TaskQuerySet.as_manager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        permissions = (
            ("can_rate_tasks", _("Can rate students tasks.")),
        )
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")

    def get_absolute_redirect_after_add_comment_url(self):
        """Return url for redirect after added comment to this task."""
        return reverse("task-detail", kwargs={"pk": self.id})


class Solution(BaseModel):
    """Solution which User can set to him task."""
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="solutions"
    )
    task = models.ForeignKey(
        to="Task",
        on_delete=models.CASCADE,
        related_name="solutions",
    )
    evaluations = models.ManyToManyField(
        to="users.User",
        blank=True,
        through="Evaluation",
    )
    solution_description = RichTextField(
        verbose_name=_("Description of solution"),
        max_length=8000,
        config_name="tasks_text"
    )
    attachment = models.FileField(
        verbose_name=_("Attachment"),
        upload_to="solutions/files/",
        null=True,
        blank=True,
    )

    objects = SolutionQuerySet.as_manager()

    def __str__(self) -> str:
        return str(self.solution_description)

    def filename(self):
        """Return attachment filename without all path."""
        return os.path.basename(self.attachment.name)

    class Meta:
        verbose_name = _("Solution")
        verbose_name_plural = _("Solutions")
        unique_together = ("task", "owner",)


class Evaluation(BaseModel):
    """Evaluation info for user solution by another user.

    This model stores information about user evaluations of current solution by
    the another user.

    Example:
        Mentor_1 and Mentor_2 evaluate User_1 solution for task number 2,
        Mentor_2 and Mentor_3 evaluate User_2 solution for task number 2,
        Mentor_1, Mentor_3 and Mentor_2 evaluate User_1 solution for task
        number 3.
    """
    mark = models.PositiveSmallIntegerField(
        verbose_name=_("Mark"),
        help_text=_(
            "Mark which user has set."
        ),
        default=5,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        null=True,
        blank=True,
    )

    comment = RichTextField(
        verbose_name=_("Comment"),
        max_length=8000,
        config_name="tasks_text",
        help_text=_(
            "Comment on the evaluation of the solution."
        )
    )
    owner = models.ForeignKey(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="owner",
        help_text=_(
            "User who evaluate this solution."
        ),
    )
    solution = models.ForeignKey(
        to="Solution",
        on_delete=models.CASCADE,
        related_name="evaluated_solution",
        help_text=_(
            "Solution that is being evaluated."
        ),
    )

    def __str__(self):
        return f"{self.owner}\'s evaluate by {self.mark}"

    class Meta:
        verbose_name = _("Evaluation info")
        verbose_name_plural = _("Evaluation info")
        unique_together = ("solution", "owner",)
