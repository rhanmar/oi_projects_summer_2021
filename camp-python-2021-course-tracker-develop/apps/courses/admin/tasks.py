from django.contrib import admin
from django.contrib.admin import ModelAdmin

from ordered_model.admin import OrderedModelAdmin

from apps.courses.admin.attachments import AttachmentInline

from .. import models


class TaskInline(admin.TabularInline):
    """InLine for Task."""

    model = models.Task


class SolutionInline(admin.TabularInline):
    """InLine for Solution."""

    model = models.Solution


class EvaluationInline(admin.TabularInline):
    """Inline for evaluation."""

    model = models.Evaluation


@admin.register(models.Task)
class TaskAdmin(OrderedModelAdmin):
    """Represent Admin interface for model Task."""

    list_display = (
        "topic",
        "title",
        "order",
        "is_hidden",
        "created_at",
        "move_up_down_links",
    )
    fields = (
        "topic",
        "title",
        "description",
        "jira_tag",
        "move_up_down_links",
        "is_hidden",
        "created_at",
        "modified_at"
    )
    list_filter = (
        "is_hidden",
        "created_at"
    )
    readonly_fields = (
        "move_up_down_links",
        "created_at",
        "modified_at"
    )
    search_fields = (
        "title",
        "description"
    )
    ordering = (
        "order",
    )

    inlines = (
        AttachmentInline,
        SolutionInline,
    )


@admin.register(models.Solution)
class Solution(ModelAdmin):
    """Represent Admin interface for model Solution."""

    list_display = (
        "solution_description",
    )

    inlines = (EvaluationInline,)
