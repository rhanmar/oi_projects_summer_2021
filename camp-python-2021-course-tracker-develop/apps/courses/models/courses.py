from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from apps.core.models import BaseDurationModel, BaseModel
from apps.courses.querysets import CourseQuerySet


class Course(BaseModel, BaseDurationModel):
    """Represent ORM model of course."""

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100
    )
    description = RichTextField(
        verbose_name=_("Description"),
        max_length=400,
        config_name="text_only"
    )
    image = ProcessedImageField(
        verbose_name=_("Image"),
        upload_to=settings.DEFAULT_MEDIA_PATH,
        processors=[ResizeToFill(width=1280, height=720)],
        options={
            "quality": 100,
        },
        default="courses/default_course_img/default.jpeg"
    )
    users = models.ManyToManyField(
        verbose_name=_("Users"),
        to="users.User",
        blank=True,
        related_name="courses"
    )
    is_hidden = models.BooleanField(
        verbose_name=_("Is hidden"),
        default=True
    )
    default_speaker = models.ForeignKey(
        verbose_name=_("Default speaker"),
        to="users.User",
        blank=True,
        null=True,
        related_name="lead_courses",
        on_delete=models.CASCADE,
    )

    # pylint: disable=[E1101]
    # Annotate in context
    def course_progress(self):
        """Return progress of user on self course.

        Progress adds up from all of chapter rating value and divide by length
        of chapters queryset.
        """
        tasks_count = self.chapters.aggregate(
            models.Count("topics__tasks")
        )["topics__tasks__count"]
        user_progress = 100 * self.count_of_marks / tasks_count
        return round(user_progress, 2)

    # pylint: disable=[E1101]
    # Annotate in context
    def course_rating(self):
        """Return rating of user on self course.

        Rating adds up from all of chapter rating value and divide by length of
        chapters queryset.
        """
        tasks_count = self.chapters.aggregate(
            models.Count("topics__tasks__solutions__evaluated_solution")
        )["topics__tasks__solutions__evaluated_solution__count"]
        user_progress = 10 * self.sum_of_marks / tasks_count
        return round(user_progress, 2)

    objects = CourseQuerySet.as_manager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
