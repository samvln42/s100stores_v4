
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from store import consumers


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oversea_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/some_path/', consumers.YourConsumer.as_asgi()),
        ])
    ),
})