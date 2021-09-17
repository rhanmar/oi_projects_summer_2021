from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from imagekit.admin import AdminThumbnail

from . import models


class UrlInline(admin.TabularInline):
    """Inline for User admin panel with urls."""

    model = models.users.Url


class SkillInline(admin.TabularInline):
    """Inline for CV admin panel with skills."""

    model = models.cvs.CVSkillEvaluation


@admin.register(models.users.User)
class UserAdmin(DjangoUserAdmin):
    """UI for User model."""

    ordering = ("email",)
    avatar_thumbnail = AdminThumbnail(image_field="avatar_thumbnail")
    list_display = (
        "avatar_thumbnail",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    list_display_links = (
        "email",
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    fieldsets = (
        (None, {
            "fields": (
                "email",
                "password"
            )
        }),
        (_("Personal info"), {
            "fields": (
                "first_name",
                "last_name",
                "avatar",
                "location",
            )
        }),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
            )
        }),
        (_("Important dates"), {
            "fields": (
                "created",
                "modified"
            )
        }),
    )
    readonly_fields = DjangoUserAdmin.readonly_fields + (
        "created",
        "modified",
    )
    search_fields = ["email", ]
    inlines = [
        UrlInline,
    ]


@admin.register(models.cvs.CV)
class CVAdmin(admin.ModelAdmin):
    """UI for CV model."""

    list_display = (
        "title",
        "description",
        "owner",
    )

    list_select_related = ("owner",)

    inlines = [
        SkillInline,
    ]


@admin.register(models.cvs.EvaluationInfo)
class EvaluationInfoAdmin(admin.ModelAdmin):
    """UI for EvaluationInfo model."""

    list_display = (
        "is_approved",
        "comment",
        "skill_from_cv",
    )
    autocomplete_fields = ("owner",)
