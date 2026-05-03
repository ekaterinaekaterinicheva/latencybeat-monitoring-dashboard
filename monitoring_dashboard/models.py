# The core blueprint for the DB.
# Building One-to-Many relationship between Statistic and DataItems.
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# The parent model (e.g., "Website Traffic)
class Statistic(models.Model):
    name = models.CharField(max_length=200)
    # A slug is a URL-friendly version of the name (e.g., "website-traffic")
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse("monitoring_dashboard:dashboard", kwargs={"slug": self.slug})
    

    @property
    def data(self): # Allows you to call 'statistic.data' to get all related DataItems
        return self.dataitem_set.all() # Adds a hidden attribute dataitem_set at runtime

    def __str__(self):
        # Tells Django how to represent this object in the Admin panel
        return str(self.name)
    
    # If no slug exists, it automatically creates one from the name before saving to the DB
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# The child model
class DataItem(models.Model):
    # Links each DataItem to one specific Statistic.
    statistic = models.ForeignKey(Statistic, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    owner = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.owner}: {self.value}"