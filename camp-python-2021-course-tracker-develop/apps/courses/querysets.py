from django.db import models
from django.db.models.functions import Coalesce

from apps.core.querysets import IsHiddenFilteringOrderedQuerySet


class CommentQuerySet(models.QuerySet):
    """Custom queryset for Comment model."""

    def parent_comments_in_reverse_order(self):
        """Return generator of parents comments sorted in reverse order."""
        return self.exclude(parent__isnull=False).order_by("-created_at")\
            .select_related("user")

    def child_comments_in_order(self):
        """Return queryset with child comments sorted by created time."""
        return self.order_by("created_at").select_related("user")


class SolutionQuerySet(models.QuerySet):
    """Custom queryset for solution model."""
    use_for_related_fields = True

    def all_with_avg_mark(self):
        """Return all solution with avg_mark annotate."""
        return self.annotate(
            avg_mark=Coalesce(models.Avg(
                "evaluated_solution__mark",
                output_field=models.FloatField(),
            ), 0.0)
        ).prefetch_related("evaluated_solution")


class TaskQuerySet(IsHiddenFilteringOrderedQuerySet):
    """Custom queryset for task model."""

    use_for_related_fields = True

    def all_with_solution_mark(self, user):
        """Return only task with solutions and with avg_mark annotate."""
        return self.filter(
            models.Q(tasks__solutions__owner=user)
        ).annotate(
            avg_mark=Coalesce(
                models.Avg(
                    "solutions__evaluated_solution__mark",
                    output_field=models.FloatField(),
                ),
                0.0,
            )
        )


class TopicQuerySet(IsHiddenFilteringOrderedQuerySet):
    """Custom queryset for topic model."""

    def all_with_solution_mark(self, user):
        """Return topics with solutions, count and sum of marks annotate."""
        return self.filter(
            models.Q(tasks__solutions__owner=user)
        ).annotate(
            count_of_marks=Coalesce(
                models.Count(
                    "tasks__solutions",
                    output_field=models.FloatField()
                ),
                0.0,
            ),
            sum_of_marks=Coalesce(
                models.Sum(
                    "tasks__solutions__evaluated_solution__mark",
                    output_field=models.FloatField()
                ),
                0.0,
            ),
        )


class ChapterQuerySet(IsHiddenFilteringOrderedQuerySet):
    """Custom queryset for chapter model."""

    def all_with_solution_mark(self, user):
        """Return chapters with solutions, count and sum of marks annotate."""
        return self.filter(
            models.Q(topics__tasks__solutions__owner=user)
        ).annotate(
            count_of_marks=Coalesce(models.Count(
                "topics__tasks__solutions",
                output_field=models.FloatField(),
            ), 0.0),
            sum_of_marks=Coalesce(models.Sum(
                "topics__tasks__solutions__evaluated_solution__mark",
                output_field=models.FloatField()
            ), 0.0),
        )


class CourseQuerySet(IsHiddenFilteringOrderedQuerySet):
    """Custom queryset for course model."""

    def all_with_solution_mark(self, user):
        """Return courses with only solutions and rating annotate."""
        return self.filter(
            models.Q(chapters__topics__tasks__solutions__owner=user)
        ).annotate(
            count_of_marks=Coalesce(models.Count(
                "chapters__topics__tasks__solutions",
                distinct=True,
                output_field=models.FloatField(),
            ), 0.0),
            sum_of_marks=Coalesce(models.Sum(
                "chapters__topics__tasks__solutions__evaluated_solution__mark",
                output_field=models.FloatField()
            ), 0.0),
        )
