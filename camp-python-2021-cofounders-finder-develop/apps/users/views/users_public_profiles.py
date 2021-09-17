from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView

from .. import models


class UserProfileView(LoginRequiredMixin, DetailView):
    """View for user profile."""
    model = models.User
    context_object_name = "user"

    template_name = "users/accounts/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk == kwargs.get("pk"):
            return HttpResponseRedirect(reverse_lazy("account"))
        return super().dispatch(request, args, kwargs)
