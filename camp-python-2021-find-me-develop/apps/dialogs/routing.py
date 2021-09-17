# chat/routing.py
from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/dialog/(?P<dialog_id>\w+)/$",
        consumers.ChatConsumer.as_asgi(),
        name="ws-chat",
    ),
    path(
        "ws/dialog-notifications/",
        consumers.DialogNotificationConsumer.as_asgi(),
        name="ws-chat-notifications",
    )
]
