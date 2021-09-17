from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from apps.core.mixins import CheckBanMixin, OwnerPermissionMixin

from .forms import MeetingForm, MeetingReviewForm
from .models import Meeting


class MainPageView(LoginRequiredMixin, CheckBanMixin, TemplateView):
    """Main page with map."""
    template_name = "map/main.html"

    EXIST_MEETING = "EXIST"
    NOT_EXIST_MEETING = "NOT_EXIST"

    def get_context_data(self, **kwargs):
        """Return custom context with form for create meeting."""
        context = super().get_context_data(**kwargs)
        context["meeting_form"] = MeetingForm()
        context["meeting_review_form"] = MeetingReviewForm()

        has_user_meeting = self.request.user.active_meetings.exists()
        context["has_visitor_meeting"] = self.NOT_EXIST_MEETING
        if has_user_meeting:
            context["has_visitor_meeting"] = self.EXIST_MEETING

        return context


class EditMeetingView(
    OwnerPermissionMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    """View for edit instance of meeting."""
    model = Meeting
    form_class = MeetingForm
    template_name = "map/edit_meeting.html"
    success_url = reverse_lazy("main_page")
    success_message = "Meeting edited successfully!"
    pk_url_kwarg = "meeting_id"
