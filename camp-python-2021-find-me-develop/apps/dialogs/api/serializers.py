from django.urls import reverse

from rest_framework import serializers

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from apps.dialogs.models import Dialog, Message
from apps.users.models import User


class DialogJoinSerializer(serializers.ModelSerializer):
    """Serializer for response for join member to Dialog."""
    class Meta:
        model = Dialog
        fields = ("dialog_url",)

    dialog_url = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_dialog_url(self, instance):
        """Return absolute url of dialog."""
        return reverse("dialog_detail", kwargs={"dialog_id": instance.id})


class SenderSerializer(serializers.ModelSerializer):
    """Serializer for dialog message sender."""

    avatar_thumbnail = serializers.URLField(
        source="avatar_thumbnail.url",
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "avatar_thumbnail",
        )


class DialogMessageSerializer(serializers.ModelSerializer):
    """Serializer for response to get a message."""

    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    sender_data = SenderSerializer(source="sender", read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "dialog",
            "text",
            "sender",
            "sender_data",
            "created",
            "modified",
        )

        read_only_fields = (
            "created",
            "modified",
            "sender_data",
        )

    def create(self, validated_data):
        """Create message with sender equal to request user.

        Check for `request` here because this serializer used in Channels
        consumer, and there are already `sender` passed to `validated_data`,
        and also, you cannot get access to `request` object because it
        doesn't exist.
        """
        if "request" in self.context:
            validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, attrs):
        user = User.objects.get(pk=self.initial_data["sender"])
        user_dialogs = Dialog.objects.filter(
            dialog_members__member=user
        )
        current_dialog = attrs.get("dialog")

        if current_dialog not in user_dialogs:
            raise serializers.ValidationError("User is not dialog member")

        return attrs


class DialogSerializer(serializers.ModelSerializer):
    """Serializer for response to get a dialog."""

    messages = DialogMessageSerializer(many=True)

    class Meta:
        model = Dialog
        fields = (
            "id",
            "title",
            "created",
            "modified",
            "messages",
        )
