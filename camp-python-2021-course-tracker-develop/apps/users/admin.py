from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from imagekit.admin import AdminThumbnail

from .models import User, UserLink

__all__ = (
    "UserAdmin",
)

from ..courses.admin.tasks import EvaluationInline


class UserLinkInline(admin.TabularInline):
    """User link inline to show user links in User admin page."""

    model = UserLink


class UserInline(admin.TabularInline):
    """InLine for Task."""

    model = User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """UI for User model."""

    ordering = ("email",)
    search_fields = ("first_name", "last_name", "email")
    profile_image_thumbnail = AdminThumbnail(
        image_field="profile_image_thumbnail"
    )
    list_display = (
        "profile_image_thumbnail",
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
                "github_username",
                "profile_image",
                "bio",
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
                "created_at",
                "modified_at"
            )
        }),
    )
    readonly_fields = DjangoUserAdmin.readonly_fields + (
        "created_at",
        "modified_at",
    )
    inlines = (
        UserLinkInline,
        EvaluationInline,
    )
