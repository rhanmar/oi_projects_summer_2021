from rest_framework import mixins, permissions
from rest_framework.pagination import CursorPagination

from django_filters.rest_framework import DjangoFilterBackend

from apps.core.api.permissions import IsDialogMember, IsMessageSender
from apps.core.api.views import BaseViewSet, ReadOnlyViewSet
from apps.dialogs.api.serializers import (
    DialogMessageSerializer,
    DialogSerializer,
)
from apps.dialogs.models import Dialog, Message


class FetchDialogMessagesPagination(CursorPagination):
    """Pagination to fetch dialog messages for chat."""
    page_size = 15
    max_page_size = 30


class DialogMessageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    BaseViewSet,
):
    """ViewSet to perform actions on dialog messages."""

    queryset = Message.objects.all()
    serializer_class = DialogMessageSerializer
    permissions_map = {
        "update": [IsMessageSender],
        "partial_update": [IsMessageSender],
        "destroy": [IsMessageSender],
    }
    pagination_class = FetchDialogMessagesPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["dialog_id"]

    def get_queryset(self):
        """Returns all messages from dialogs where user has a membership."""
        user_dialogs = Dialog.objects.filter(
            dialog_members__member=self.request.user
        )
        return self.queryset.filter(dialog__in=user_dialogs)


class DialogViewSet(ReadOnlyViewSet):
    """ViewSet to perform actions on dialogs."""
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsDialogMember,
    ]
