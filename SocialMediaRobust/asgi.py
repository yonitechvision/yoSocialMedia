"""
ASGI config for SocialMediaRobust project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
#from SocialMediaRobust.api.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from api.consumers import VideoCallConsumer
from django.urls import path  # You need to import path for WebSocket routing

# Set the default settings module for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialMediaRobust.settings')

# Initialize the ASGI application for HTTP and WebSocket protocols
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP handling
    "websocket": AuthMiddlewareStack(  # WebSocket handling with authentication
        URLRouter([
            path('ws/call/<room_name>/', VideoCallConsumer.as_asgi()),  # WebSocket URL route
        ])
    ),
})
