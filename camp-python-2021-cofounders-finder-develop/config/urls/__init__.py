from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

admin.site.site_header = settings.APP_LABEL

urlpatterns = [
    path("admin/", admin.site.urls),
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    path("", include("apps.core.urls")),
    path("health/", include("health_check.urls")),
    path("users/", include("apps.users.urls")),
    path("startups/", include("apps.startups.urls")),
    path(r'search/', include('haystack.urls')),
    path("chat/", include("apps.chat.urls"))
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
