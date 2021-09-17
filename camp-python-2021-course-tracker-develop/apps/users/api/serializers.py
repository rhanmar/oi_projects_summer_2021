from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

from apps.core.api.serializers import BaseSerializer
from apps.users.models import User


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


class PublicUserSerializer(ModelSerializer):
    """Represent public user serializer."""

    class Meta:
        model = User
        fields = (
            "get_full_name",
            "profile_image",
        )
