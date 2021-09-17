from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from apps.core.mixins import CheckBanBlacklistMixin
from apps.users.forms import UserReportForm
from apps.users.models import User


class UserAddReportView(
    LoginRequiredMixin,
    CheckBanBlacklistMixin,
    SuccessMessageMixin,
    CreateView
):
    """View for add Report."""

    template_name = "users/user_add_report.html"
    form_class = UserReportForm
    success_url = reverse_lazy("user_profile")
    success_message = "The new report was created successfully!"
    extra_context = {
        "title": "report",
        "form_header": "Report",
        "submit_text": "Add",
    }

    def dispatch(self, request, *args, **kwargs):
        """Check that visitor not profile owner."""
        profile_owner_id = self.kwargs["user_id"]
        if profile_owner_id == request.user.id:
            return HttpResponseForbidden(
                "You cannot add report for yourself."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Return custom context with reported fullname and page title."""
        context = super().get_context_data(**kwargs)
        reported_id = self.kwargs["user_id"]
        context["reported_user"] = User.objects.get(id=reported_id)
        return context

    def get_success_url(self):
        """Return success redirect url to profile of reported user."""
        reported_id = self.kwargs["user_id"]
        return reverse("user_profile", kwargs={"user_id": reported_id})

    def get_form_kwargs(self):
        """Send user request params to form init as kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "created_by_id": self.request.user.id,
            "reported_id": self.kwargs["user_id"]}
        )
        return kwargs
