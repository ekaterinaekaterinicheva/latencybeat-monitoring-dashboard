from django.urls import path
from .views import main, dashboard

app_name = "monitoring_dashboard"

urlpatterns = [
    path('', main, name='main'),
    path('<slug>/', dashboard, name='dashboard'),
]
