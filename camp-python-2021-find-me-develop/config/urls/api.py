from django.urls import include, path
from watson.views import SearchApiView

app_name = "api"


urlpatterns = [
    # API URLS
    path("auth/", include("apps.users.api.auth.urls")),
    path("dialogs/", include("apps.dialogs.api.urls")),
    path("users/", include("apps.users.api.urls")),
    path("map/", include("apps.map.api.urls")),
    path("search/", SearchApiView.as_view(), name="search"),
]
