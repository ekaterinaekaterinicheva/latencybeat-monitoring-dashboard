from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic, DataItem

def main(request):
    qs = Statistic.objects.all()

    if request.method == "POST":
        new_stat = request.POST.get("new-statistic")

        # Check: Create ONLY IF the user actually typed something
        if new_stat and new_stat.strip():
            obj, created = Statistic.objects.get_or_create(name=new_stat)
            # Redirect to the dashboard of the newly created (or existing) device
            return redirect("monitoring_dashboard:dashboard", slug=obj.slug)
    
    return render(request, "monitoring_dashboard/main.html", {'qs': qs})

def dashboard(request, slug):
    # Fetch the device or return a 404 error if it doesn't exist
    obj = get_object_or_404(Statistic, slug=slug)

    # Get the last 20 data points to "prime" the chart
    historical_data = DataItem.objects.filter(statistic=obj).order_by('-created_at')[:20]

    # Reverse them so they are in chronological order (oldest to newest)
    historical_data = reversed(historical_data)

    return render(request, "monitoring_dashboard/dashboard.html", {
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data, # Calls the @property from the models.py
        'historical_data': historical_data
    })
