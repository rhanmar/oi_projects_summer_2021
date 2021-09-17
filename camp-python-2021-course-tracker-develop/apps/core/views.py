from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    """Render main page."""

    template_name = "index/index.html"
