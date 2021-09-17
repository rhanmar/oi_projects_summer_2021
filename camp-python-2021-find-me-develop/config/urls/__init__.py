from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from watson.views import SearchView

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

admin.site.site_header = settings.APP_LABEL

urlpatterns = [
    path("admin/", admin.site.urls),
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    path("health/", include("health_check.urls")),
    path("map/", include("apps.map.urls")),
    path("", include("apps.users.urls")),
    path("dialogs/", include("apps.dialogs.urls")),
    path(
        "search/",
        SearchView.as_view(template_name="search/search_results.html"),
        name="search",
    ),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
