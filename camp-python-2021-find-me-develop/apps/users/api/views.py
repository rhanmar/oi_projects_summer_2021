from django.contrib.auth import get_user_model

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.core.api.permissions import IsBannedUser, IsUserReviewCreator
from apps.core.api.views import BaseViewSet
from apps.dialogs.api.serializers import DialogJoinSerializer
from apps.dialogs.models import Dialog, DialogMember
from apps.users.models import Review

from . import serializers

User = get_user_model()


class UserInfoViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    BaseViewSet
):
    """ViewSet for viewing users, start dialog with user."""

    queryset = User.objects.all()
    serializer_class = serializers.UserInfoSerializer
    serializers_map = {
        "list": serializers.UserDetailSerializer,
        "join": DialogJoinSerializer,
    }
    permissions_map = {
        "list": (AllowAny, IsBannedUser,),
    }

    def get_queryset(self):
        """Return queryset of Users with rating for 'retrieve' requests."""
        queryset = super().get_queryset()
        if self.action == "retrieve":
            return queryset.with_rating()
        return queryset

    @action(detail=True, methods=["post"])
    def join(self, request, *args, **kwargs):
        """Start dialog with user."""
        first_user_id = request.user.id
        second_user = self.get_object()
        has_users_dialog = Dialog.objects.exclude(
            meeting__isnull=False
        ).filter(
            dialogmember__member_id=first_user_id
        ).filter(
            dialogmember__member_id=second_user.id
        )

        if has_users_dialog.exists():
            dialog = has_users_dialog.first()
        else:
            second_user_name = second_user.get_fullname()
            dialog_title = (
                f"{request.user.get_fullname()} - {second_user_name}"
            )
            dialog = Dialog.objects.create(title=dialog_title)
            DialogMember.objects.create(
                dialog_id=dialog.id, member_id=first_user_id
            )
            DialogMember.objects.create(
                dialog_id=dialog.id, member_id=second_user.id
            )

        serializer = self.get_serializer(instance=dialog)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )


class UserReviewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet
):
    """ViewSet for viewing reviews."""

    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsUserReviewCreator,)
    permissions_map = {
        "list": (AllowAny, IsBannedUser,),
        "retrieve": (AllowAny, IsBannedUser),
    }

    @action(detail=False, methods=["GET"])
    def from_me(self, request, *args, **kwargs):
        """Return list of reviews from current user."""
        current_user_reviews = request.user.reviews.all()
        serializer = self.get_serializer(
            instance=current_user_reviews,
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["GET"])
    def to_me(self, request, *args, **kwargs):
        """Return list of reviews about current user."""
        current_user_reviews = request.user.reviews_of.all()
        serializer = self.get_serializer(
            instance=current_user_reviews,
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
