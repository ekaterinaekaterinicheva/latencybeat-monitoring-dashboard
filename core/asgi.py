"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set settings and initialize the Django ASGI application 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django_asgi_app = get_asgi_application()

# Import Channels components
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import monitoring_dashboard.routing

# Define the main application entry point
application = ProtocolTypeRouter(
    {
        # Standard HTTP traffic handled by Django
        "http": django_asgi_app,

        # WebSocket traffic handled by Channels
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    monitoring_dashboard.routing.websocket_urlpatterns
                )
            )
        ),
    }
)