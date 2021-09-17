import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import django
django.setup()
from apps.websockets import routing as django_channels_routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            django_channels_routing.websocket_urlpatterns
        )

    ),
})
