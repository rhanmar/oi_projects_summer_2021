from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from ordered_model.models import OrderedModel

from apps.core.models import BaseModel
from apps.courses.models import Comment
from apps.courses.querysets import TopicQuerySet


class Topic(BaseModel, OrderedModel):
    """Represent ORM model of topic."""

    order_with_respect_to = "chapter"

    chapter = models.ForeignKey(
        verbose_name=_("Chapter"),
        to="courses.Chapter",
        on_delete=models.CASCADE,
        related_name="topics"
    )
    tags = models.ManyToManyField(
        verbose_name=_("Tags"),
        to="courses.Tag",
        related_name="topics",
        blank=True
    )
    speaker = models.ForeignKey(
        verbose_name=_("Speaker"),
        to="users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="topics"
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=100,
    )
    description = RichTextField(
        verbose_name=_("Description"),
        max_length=400,
        null=True,
        blank=True,
        config_name="text_only"
    )
    reading_date = models.DateField(
        verbose_name=_("Reading date"),
        auto_now_add=True,
        null=True,
        blank=True,
    )
    comments = GenericRelation(Comment)

    objects = TopicQuerySet.as_manager()

    # pylint: disable=[E1101]
    # Annotate in context
    def topic_rating(self):
        """Return rating of user on self topic.

        Rating adds up from all of tasks rating value and divide by length
        of tasks queryset.
        """
        evaluations_count = self.tasks.aggregate(
            models.Count("solutions__evaluated_solution")
        )["solutions__evaluated_solution__count"]
        if not evaluations_count:
            return 0.0
        topic_mark = 10 * self.sum_of_marks / evaluations_count
        return round(topic_mark, 2)

    # pylint: disable=[E1101]
    # Annotate in context
    def topic_progress(self):
        """Return progress of user on self topic.

        Progress adds up from all of tasks progress value and divide by length
        of tasks queryset.
        """
        if not self.tasks.count():
            return 0.0
        topic_rating = 100 * self.count_of_marks / self.tasks.count()
        return round(topic_rating, 2)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ("reading_date",)

    def get_absolute_redirect_after_add_comment_url(self):
        """Return redirect url after added comment to this topic."""
        return reverse("topic-detail", kwargs={"pk": self.id})
