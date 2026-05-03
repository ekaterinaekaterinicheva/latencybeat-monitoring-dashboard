from django.shortcuts import render
from .models import Statistic, DataItem

def main(request):
    qs = Statistic.objects.all()
    return render(request, "monitoring_dashboard/main.html", {'qs': qs})

def dashboard(request, slug):
    return render(request, "monitoring_dashboard/dashboard.html", {})
