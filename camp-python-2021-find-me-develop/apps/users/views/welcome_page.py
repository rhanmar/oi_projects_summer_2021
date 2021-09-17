from django.views.generic import TemplateView

from apps.core.mixins import RedirectLoggedInUsersMixin


class IndexView(RedirectLoggedInUsersMixin, TemplateView):
    """View for welcome page."""

    template_name = "users/index.html"
