from django.utils import timezone
from django.db import models

class TourModel(models.Model):

    tour_name = models.CharField(max_length=15)
    tour_location = models.TextField()
    start_date = models.DateField(default=timezone.now())
    end_date = models.DateField(default=timezone.now())
    tour_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    description = models.TextField()
    tour_brand = models.CharField(max_length=15, blank=True)
    tour_budg_fooddrink = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tour_budg_transpt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tour_budg_others = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateField(default=timezone.now())
    updated_at = models.DateField(default=timezone.now())
    def __str__(self)->str:
         return self.tour_name
