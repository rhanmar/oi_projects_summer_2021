from django.contrib import admin

from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """UI for Skill model."""

    ordering = ("name", )
    list_display = (
        "name",
    )
