from django.urls import re_path
from typing import Any, cast
from .consumers import DashboardConsumer

websocket_urlpatterns = [
    re_path(r'^ws/(?P<dashboard_slug>[\w-]+)/$', cast(Any, DashboardConsumer.as_asgi())),
]