import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from apps.dialogs import routing as dialogs_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            dialogs_routing.websocket_urlpatterns
        )
    ),
})
