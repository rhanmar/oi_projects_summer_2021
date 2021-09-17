from django.contrib import admin

from imagekit.admin import AdminThumbnail

from .models import Attachment, Dialog, DialogMember, Message


@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    """UI for Dialog model."""
    logo_thumbnail = AdminThumbnail(image_field="logo_thumbnail")
    list_display = (
        "title",
        "logo_thumbnail",
    )
    list_display_links = (
        "title",
    )
    readonly_fields = (
        "created",
        "modified",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """UI for Message model."""
    list_display = (
        "text",
        "sender_id",
        "dialog_id",
    )
    list_display_links = (
        "text",
    )
    readonly_fields = (
        "created",
        "modified",
    )


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    """UI for Attachment model."""
    list_display = (
        "file",
        "message_id",
    )
    list_display_links = (
        "file",
    )
    readonly_fields = (
        "created",
        "modified",
    )


@admin.register(DialogMember)
class DialogMemberAdmin(admin.ModelAdmin):
    """UI for DialogMember model."""
    list_display = (
        "dialog_id",
        "member_id",
    )
    readonly_fields = (
        "created",
        "modified",
    )
