from django.db import transaction

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.core.api.permissions import (
    IsBannedUser,
    IsMeetingReviewOwner,
    IsOwnerMeeting,
)
from apps.core.api.views import BaseViewSet
from apps.dialogs.api.serializers import DialogJoinSerializer
from apps.dialogs.models import DialogMember
from apps.map.models import Location, Meeting, MeetingReview

from .serializers import (
    LocationSerializer,
    MeetingCreateSerializer,
    MeetingDetailSerializer,
    MeetingReviewSerializer,
    UserLocationSerializer,
)


class LocationViewSet(
    mixins.ListModelMixin,
    BaseViewSet,
):
    """View for get all locations created for map."""
    queryset = Location.objects.fresh_all_locations()
    serializer_class = LocationSerializer
    serializers_map = {
        "change_user_location": UserLocationSerializer,
    }

    def get_queryset(self):
        """Return queryset.

        This function returns queryset with all locations only for
        user with is_visible and also show meetings for the current user from
        users who didn't banned him.

        """
        current_user_banned_by = self.request.user.banned_by.values_list(
            "user",
            flat=True
        )
        queryset = super().get_queryset()
        queryset = queryset.exclude(
            meeting__created_by__in=current_user_banned_by
        )
        is_visible = self.request.user.is_visible
        if is_visible:
            return queryset
        return queryset.meeting_points()

    @action(detail=False, methods=["post"])
    def change_user_location(self, request, *args, **kwargs):
        """Create or update user location and return the Location obj."""
        serializer = self.get_serializer(
            data=request.data, instance=request.user.location,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class MeetingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """View set for create, get all, get one Meetings."""

    queryset = Meeting.objects.all()
    serializer_class = MeetingDetailSerializer
    serializers_map = {
        "create": MeetingCreateSerializer,
        "join": DialogJoinSerializer,
    }
    permissions_map = {
        "update": (IsOwnerMeeting, IsBannedUser,),
        "partial_update": (IsOwnerMeeting, IsBannedUser,),
        "destroy": (IsOwnerMeeting, IsBannedUser,),
    }

    def perform_create(self, serializer):
        """Perform atomic creation of meeting with location."""
        with transaction.atomic():
            super().perform_create(serializer)

    def perform_destroy(self, instance):
        """Delete meeting location with meeting.

        Meeting has one-to-one related field to Location
        that has on_delete=CASCADE. So, delete location will delete meeting.

        """
        instance.location.delete()

    @action(detail=True, methods=["post"])
    def join(self, request, *args, **kwargs):
        """Check count people in the meeting and join user to it.

        Joining is skipped if user has already joined to the dialog.
        Check that current user is not in blacklist.
        Check that current user is not banned.

        """
        meeting = self.get_object()

        if request.user.id == meeting.created_by_id:
            return Response(
                "You can't join your own meeting",
                status=status.HTTP_403_FORBIDDEN
            )

        is_banned_by_meeting_owner = meeting.created_by.banned.filter(
            banned_user_id=self.request.user.id
        ).exists()
        if is_banned_by_meeting_owner:
            return Response(status=status.HTTP_403_FORBIDDEN)

        dialog = meeting.dialog
        user_id = request.user.id
        is_user_dialog_member = dialog.dialog_members.filter(
            member_id=user_id
        ).exists()

        if not is_user_dialog_member:
            max_people_in_meeting = meeting.max_people_limit
            count_people_in_meeting = dialog.dialog_members.count()

            if max_people_in_meeting <= count_people_in_meeting:
                return Response(
                    "Dialog is already full.",
                    status=status.HTTP_403_FORBIDDEN,
                )

            DialogMember.objects.create(
                dialog_id=dialog.id, member_id=user_id
            )

        serializer = self.get_serializer(instance=dialog)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=True, methods=["post"])
    def leave(self, request, *args, **kwargs):
        """Delete current user from meeting."""
        meeting = self.get_object()

        user_as_dialog_member = DialogMember.objects.filter(
            member=request.user,
            dialog=meeting.dialog
        )

        if not user_as_dialog_member.exists():
            data = {"error": "You're not a member of this meeting."}
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        user_as_dialog_member.delete()
        return Response(
            {"detail": "Successfully deleted from dialog"},
            status=status.HTTP_200_OK,
        )


class MeetingReviewViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    BaseViewSet,
):
    """Viewset to perform actions on meeting review."""

    queryset = MeetingReview.objects.all()
    serializer_class = MeetingReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["meeting", "created_by"]
    permissions_map = {
        "destroy": [IsMeetingReviewOwner],
        "update": [IsMeetingReviewOwner],
        "partial_update": [IsMeetingReviewOwner],
    }
