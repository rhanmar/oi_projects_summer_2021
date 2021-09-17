from django.urls import path, re_path

from apps.websockets.consumers import NotificationConsumer

from .consumers import CommentsConsumer

websocket_urlpatterns = [
    path(
        "ws/comments/<str:model_name>/<int:pk>/",
        CommentsConsumer.as_asgi(),
    ),
    re_path(
        r"ws/notifications/(?P<token>\w+)/$",
        NotificationConsumer.as_asgi()
    )
]
