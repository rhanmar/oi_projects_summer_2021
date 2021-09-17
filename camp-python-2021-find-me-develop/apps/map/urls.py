from django.urls import path

from apps.map.views import EditMeetingView, MainPageView

urlpatterns = [
    path("", MainPageView.as_view(), name="main_page"),
    path(
        "meeting/<int:meeting_id>/",
        EditMeetingView.as_view(),
        name="edit_meeting"
    ),
]
