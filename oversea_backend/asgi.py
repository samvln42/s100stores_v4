# asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from oversea_backend import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oversea_backend.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/some_path/', consumers.YourConsumer.as_asgi()),
        ])
    ),
})
