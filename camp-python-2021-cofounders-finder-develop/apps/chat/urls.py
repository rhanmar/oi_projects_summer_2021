from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.ChatMainPageView.as_view(),
        name="chat_main_page",
    ),
    path(
        "<int:user_pk>/",
        views.ChatRoomView.as_view(),
        name="chat_room",
    ),
]
