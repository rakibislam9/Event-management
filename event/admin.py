from django.contrib import admin
from .models import Event, category, Booking

# Register your models here.


admin.site.register(Event)
admin.site.register(category)
admin.site.register(Booking)
