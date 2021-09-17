from typing import Union

from django.contrib.gis.geos import Point

from rest_framework import serializers

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from apps.dialogs.models import Dialog, DialogMember
from apps.map.constants import PointTypeChoices
from apps.map.models import Location, Meeting, MeetingReview


def validate_str_to_point(value):
    """Validate value and return new Point if value is correct."""
    split_location = value.split(",")
    if len(split_location) != 2:
        raise serializers.ValidationError(
            "location has not two coordinates."
        )
    try:
        coords = list(map(float, split_location))
    except ValueError as err:
        raise serializers.ValidationError(
            "Coords must be a float type"
        ) from err
    point = Point(coords)
    return point


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model."""

    point = serializers.ListField(
        source="point.coords",
        read_only=True,
        child=serializers.FloatField(),
    )
    linked_id = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = ("title", "point", "point_type", "linked_id",)

    @extend_schema_field(OpenApiTypes.INT)
    def get_linked_id(self, instance):
        """Get id one-to-one linked object with location."""
        if hasattr(instance, "user"):
            return instance.user.id
        if hasattr(instance, "meeting"):
            return instance.meeting.id
        return -1


class UserLocationSerializer(serializers.ModelSerializer):
    """Serializer for upload user location."""

    user_coords = serializers.CharField()

    class Meta:
        model = Location
        fields = ("user_coords",)

    def validate_user_coords(self, value):
        """Check that value have correct format and return created Point."""
        return validate_str_to_point(value)

    def create(self, validated_data):
        """Create new user location."""
        point = validated_data["user_coords"]
        user = self.context["request"].user
        location = Location.objects.create(
            title=user.get_fullname(),
            point=point,
            point_type=PointTypeChoices.USER_POINT,
            user=user,
        )
        return location

    def update(self, instance, validated_data):
        """Update already exist user location."""
        point = validated_data["user_coords"]
        instance.point = point
        instance.save()
        return instance


class MeetingCreateSerializer(serializers.ModelSerializer):
    """Serializer for create Meeting model."""

    location_add = serializers.CharField(write_only=True)
    location = LocationSerializer(read_only=True)
    max_people_limit = serializers.IntegerField(min_value=1)

    class Meta:
        model = Meeting
        fields = (
            "title",
            "description",
            "max_people_limit",
            "photo",
            "deadline",
            "location",
            "location_add",
        )

    def validate_location_add(self, value):
        """Check that location has correct format and return created Point."""
        return validate_str_to_point(value)

    def create(self, validated_data):
        """Rewrite validated_data and return instance of Meeting."""
        location_point = validated_data.pop("location_add")
        location = Location.objects.create(
            title=validated_data["title"],
            point=location_point,
        )
        validated_data["location_id"] = location.id

        user_id = self.context["request"].user.id
        validated_data["created_by_id"] = user_id

        dialog = Dialog.objects.create(title=validated_data["title"])
        validated_data["dialog_id"] = dialog.id
        DialogMember.objects.create(
            dialog_id=dialog.id, member_id=user_id
        )

        return super().create(validated_data)


class MeetingDetailSerializer(serializers.ModelSerializer):
    """Serializer for instance of Meeting."""

    created_by = serializers.IntegerField(source="created_by_id")
    deadline = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    max_people_limit = serializers.IntegerField(min_value=1)
    dialog_members_count = serializers.IntegerField(
        source="dialog.dialog_members.count",
        read_only=True,
    )
    current_user_review_id = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.ANY)
    def get_current_user_review_id(
        self,
        instance: Meeting,
    ) -> Union[int, None]:
        """Get user's review id for meeting instance.

        Returns:
            User review id if exists, otherwise None.
        """
        user_review = instance.reviews.filter(
            created_by=self.context["request"].user,
        )

        if user_review.exists():
            return user_review.first().id

        return None

    class Meta:
        model = Meeting
        fields = (
            "id",
            "title",
            "description",
            "max_people_limit",
            "photo",
            "deadline",
            "created_by",
            "dialog_members_count",
            "current_user_review_id",
        )


class MeetingReviewSerializer(serializers.ModelSerializer):
    """Serializer for instance of MeetingReview."""

    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    meeting = serializers.PrimaryKeyRelatedField(
        queryset=Meeting.objects.all()
    )

    class Meta:
        model = MeetingReview
        fields = (
            "id",
            "title",
            "body",
            "rate",
            "created_by",
            "meeting",
        )

    def create(self, validated_data):
        """Create review with request.user as creator."""
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

    def validate_meeting(self, value):
        """Check if meeting review on specified meeting already exists."""
        current_user = self.context["request"].user
        user_reviews_on_meeting = MeetingReview.objects.filter(
            meeting=value, created_by=current_user
        )
        if user_reviews_on_meeting.exists():
            raise serializers.ValidationError(
                "Review already exists."
            )
        return value
