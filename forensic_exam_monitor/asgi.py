# asgi.py

from .wsgi import *
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .urls import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forensic_exam_monitor.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # Directly import websocket_urlpatterns from urls.py
            websocket_urlpatterns
        )
    ),
})
