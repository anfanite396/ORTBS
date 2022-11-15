from django.contrib import admin

# Register your models here.

from .models import Restaurant, TableBooking

admin.site.register(Restaurant)
admin.site.register(TableBooking)
