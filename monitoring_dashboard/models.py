# The core blueprint for the DB.
# Building One-to-Many relationship between Statistic and DataItems.
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# The parent model (e.g., "Website Traffic)
class Statistic(models.Model):
    name = models.CharField(max_length=200)
    # A slug is a URL-friendly version of the name (e.g., "website-traffic")
    slug = models.SlugField(blank=True, unique=True)

    def get_absolute_url(self):
        return reverse("monitoring_dashboard:dashboard", kwargs={"slug": self.slug})

    @property
    def data(self):
        # Returns all health records linked to this device; newest records first
        return self.dataitem_set.all().order_by('-created_at') # Adds a hidden attribute dataitem_set at runtime

    def __str__(self):
        # Tells Django how to represent this object in the Admin panel
        return str(self.name)
    
    def save(self, *args, **kwargs):
        # If no slug exists, it creates one from the name before saving to the DB
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# The child model
class DataItem(models.Model):
    # Links each DataItem to one specific Statistic.
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    value = models.PositiveIntegerField() # E.g.: Latency (in ms)
    owner = models.CharField(max_length=200) # E.g.:"System Ping" or "Manual User"
    created_at = models.DateTimeField(auto_now_add=True) # Records the time when this data arrived

    def __str__(self):
        return f"{self.statistic.name} - {self.value}ms ({self.created_at})"