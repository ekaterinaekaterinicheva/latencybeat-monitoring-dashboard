from django.urls import re_path
from typing import Any, cast
from .consumers import DashboardConsumer

# This list tells Channels which consumer to trigger based on the URL
websocket_urlpatterns = [
    # A regex path is used to capture the 'dashboard_slug' from the URL
    # Ex.: ws://127.0.0.1:8000/ws/server-1/
    re_path(r'^ws/(?P<dashboard_slug>[\w-]+)/$',
            cast(Any, DashboardConsumer.as_asgi()) # cast(Any) prevents Pylance from complaining about as_asgi()
    ),
]