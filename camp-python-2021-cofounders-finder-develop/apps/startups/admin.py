from django.contrib import admin

from apps.comments.models import Comment
from apps.core.admin import BaseAdmin

from . import models


class VacancyInline(admin.TabularInline):
    """InLine for Vacancy."""

    model = models.Vacancy


class EmployeeInline(admin.TabularInline):
    """InLine for Employee."""

    model = models.Employee


class RequestInline(admin.TabularInline):
    """InLine for Request."""

    model = models.Request


class CommentInline(admin.TabularInline):
    """InLine for Comment."""

    model = Comment


@admin.register(models.Startup)
class StartupAdmin(BaseAdmin):
    """UI for Startup model."""

    ordering = ("title",)
    list_display = (
        "title",
        "status",
        "created",
        "start_date",
        "end_date",
        "text",
        "owner",
        "slug",
    )
    list_select_related = ("owner",)
    autocomplete_fields = ("owner",)

    inlines = (
        VacancyInline,
        CommentInline,
    )


@admin.register(models.Vacancy)
class VacancyAdmin(BaseAdmin):
    """UI for Vacancy model."""

    ordering = ("title",)
    list_display = (
        "title",
        "status",
        "description",
        "startup",
    )
    list_select_related = ("startup",)
    filter_horizontal = ("skills",)
    inlines = (
        EmployeeInline,
        RequestInline,
    )


@admin.register(models.Employee)
class EmployeeAdmin(BaseAdmin):
    """UI for Employee model."""

    list_display = (
        "user",
        "vacancy",
    )
    list_select_related = (
        "vacancy",
        "user",
    )


@admin.register(models.Request)
class RequestAdmin(BaseAdmin):
    """UI for Request model."""

    list_display = (
        "user",
        "vacancy",
        "status",
        "message",
    )
    list_select_related = (
        "vacancy",
        "user",
    )
