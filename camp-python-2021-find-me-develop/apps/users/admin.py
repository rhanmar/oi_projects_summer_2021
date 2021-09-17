from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from imagekit.admin import AdminThumbnail

from .models import BlackList, Review, User, UserReport


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """UI for User model."""
    ordering = ("email", )
    avatar_thumbnail = AdminThumbnail(image_field="avatar_thumbnail")
    list_display = (
        "avatar_thumbnail",
        "email",
        "first_name",
        "last_name",
        "bio",
        "is_banned",
        "is_visible",
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
                "bio",
            )
        }),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_banned",
                "is_visible",
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


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    """UI for BlackList model."""
    list_display = ("user", "banned_user")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """UI for Review model."""


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    """UI for UserReport model."""
