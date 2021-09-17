from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView

from apps.users.models import User

from .models import Dialog, Message


class ChatMainPageView(LoginRequiredMixin, TemplateView):
    """Get main page for chat."""
    template_name = "chat/main.html"

    def get_context_data(self, **kwargs):
        """Return updated context with list of dialog for current user."""
        context = super().get_context_data(**kwargs)
        context["dialogs"] = Dialog.get_dialogs_for_user(self.request.user)
        return context


class ChatRoomView(LoginRequiredMixin, ListView):
    """Get dialog between two users and old messages."""
    template_name = "chat/room.html"
    paginate_by = 10
    context_object_name = "messages"

    def get_context_data(self, **kwargs):
        """Return updated context with receiver and dialogs."""
        context = super().get_context_data(**kwargs)
        receiver = User.objects.filter(pk=self.kwargs["user_pk"]).first()
        context["receiver"] = receiver
        context["dialogs"] = Dialog.get_dialogs_for_user(self.request.user)
        return context

    def get_queryset(self):
        return Message.get_messages_for_dialog(
            sender=self.request.user.pk,
            recipient=self.kwargs["user_pk"],
        )
