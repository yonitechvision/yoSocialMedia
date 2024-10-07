# SocialMediaRobust/routing.py
from django.urls import path
from api.consumers import VideoCallConsumer  # Import the consumer from the api directory

# Define WebSocket URL patterns
websocket_urlpatterns = [
    path('ws/call/<str:room_name>/', VideoCallConsumer.as_asgi()),  # Use room_name as the dynamic part
]

