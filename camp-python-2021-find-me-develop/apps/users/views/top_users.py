from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.core.mixins import CheckBanMixin
from apps.users.models import User


class TopUsersView(LoginRequiredMixin, CheckBanMixin, ListView):
    """List of top users with the highest rating."""

    template_name = "users/top_users.html"
    context_object_name = "users"
    queryset = User.objects.get_top_users()
