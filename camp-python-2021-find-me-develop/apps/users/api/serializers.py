from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.core.api.serializers import BaseSerializer
from apps.users.models import Review, User


class UserDetailSerializer(BaseSerializer):
    """Serializer for representing `User`."""

    class Meta:
        model = get_user_model()
        exclude = (
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
        )
        read_only_fields = ("email", )
        extra_kwargs = {
            "email": {"required": False},
        }


class UserInfoSerializer(serializers.ModelSerializer):
    """Serializer for information about user."""

    fullname = serializers.CharField(source="get_fullname")
    rating = serializers.FloatField()

    class Meta:
        model = User
        fields = ("fullname", "email", "avatar", "rating",)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for representing Review."""

    class Meta:
        model = Review
        fields = (
            "id",
            "title",
            "body",
            "rate",
            "reviewer",
            "reviewed",
        )
