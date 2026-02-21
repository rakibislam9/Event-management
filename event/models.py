from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
    


class Event(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.PositiveIntegerField()
    available_seates = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")
    booked_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.user.username} - {self.event.title}"