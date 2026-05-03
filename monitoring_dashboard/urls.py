from django.urls import path
from .views import main, dashboard

app_name = "monitoring_dashboard"

urlpatterns = [
    path('', main, name='main'), # Home page: list and add devices
    path('<slug:slug>/', dashboard, name='dashboard'), # Dashboard page: details for a device using its slug
]