from django.contrib import admin

from .models.tour_model import TourModel

from .models.user_model import Users

# Register your models here.
admin.site.register([Users, TourModel])