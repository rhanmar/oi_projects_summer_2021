from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns

admin.site.site_header = settings.APP_LABEL

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("github/", include("apps.github.urls")),
    path("", include("apps.courses.urls")),
    # Django Health Check url
    # See more details: https://pypi.org/project/django-health-check/
    path("health/", include("health_check.urls")),
    # CKEditor url
    # See more details: https://github.com/django-ckeditor/django-ckeditor
    path("ckeditor/", include('ckeditor_uploader.urls')),
]

urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
