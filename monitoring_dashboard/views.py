from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic, DataItem

def main(request):
    qs = Statistic.objects.all()
    if request.method == "POST":
        new_stat = request.POST.get("new-statistic")
        obj, _ = Statistic.objects.get_or_create(name=new_stat)
        return redirect("monitoring_dashboard:dashboard", obj.slug)
    return render(request, "monitoring_dashboard/main.html", {'qs': qs})

def dashboard(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    return render(request, "monitoring_dashboard/dashboard.html", {
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data
        })
