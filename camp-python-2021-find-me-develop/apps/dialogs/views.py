import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.mixins import CheckBanMixin


class DialogDetailView(LoginRequiredMixin, CheckBanMixin, TemplateView):
    """View for detail dialog between users."""
    template_name = "dialogs/dialog.html"

    def get_context_data(self, **kwargs):
        """Extend basic context data.

        Appends json_user_id and json_dialog_id to parse it from template
        with js function and pass to Vue script.
        """
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["json_user_id"] = json.dumps(self.request.user.id)
        context["json_dialog_id"] = json.dumps(kwargs.get("dialog_id"))
        return context
