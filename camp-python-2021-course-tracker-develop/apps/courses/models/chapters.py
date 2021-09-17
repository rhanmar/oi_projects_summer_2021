from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from apps.core.models import BaseDurationModel, BaseModel, BaseOrderedModel
from apps.courses.querysets import ChapterQuerySet


class Chapter(
    BaseModel,
    BaseOrderedModel,
    BaseDurationModel,
):
    """Represent ORM model of chapter."""

    order_with_respect_to = "course"

    course = models.ForeignKey(
        verbose_name=_("Course"),
        to="courses.Course",
        on_delete=models.CASCADE,
        related_name="chapters"
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100
    )
    description = RichTextField(
        verbose_name=_("Description"),
        max_length=400,
        null=True,
        blank=True,
        config_name="text_only"
    )
    is_hidden = models.BooleanField(
        verbose_name=_("Is hidden"),
        default=False
    )

    objects = ChapterQuerySet.as_manager()

    # pylint: disable=[E1101]
    # Annotate in context
    def chapter_progress(self):
        """Return progress of user on self chapter.

        Progress adds up from all of topics progress value and divide by
        length of topics queryset.
        """
        tasks_count = self.topics.aggregate(
            models.Count("tasks")
        )["tasks__count"]
        chapter_progress = 100 * self.count_of_marks / tasks_count
        return round(chapter_progress, 2)

    # pylint: disable=[E1101]
    # Annotate in context
    def chapter_rating(self):
        """Return rating of user on self chapter.

        Rating adds up from all of topics rating value and divide by length
        of topics queryset.
        """
        tasks_count = self.topics.aggregate(
            models.Count("tasks__solutions__evaluated_solution")
        )["tasks__solutions__evaluated_solution__count"]
        chapter_progress = 10 * self.sum_of_marks / tasks_count
        return round(chapter_progress, 2)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Chapter")
        verbose_name_plural = _("Chapters")
        ordering = ("order",)
