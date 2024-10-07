"""
URL configuration for SocialMediaRobust project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Corrected import for websocket_urlpatterns
from SocialMediaRobust.routing import websocket_urlpatterns

from django.contrib import admin
from django.urls import path, include
from channels.routing import ProtocolTypeRouter, URLRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include your app's URLs
    
    # JWT Token Generation URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # For obtaining token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # For refreshing token
]

from django.conf import settings
from django.conf.urls.static import static

# Add this at the end of your main urls.py file
if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
