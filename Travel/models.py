from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Bus(models.Model):
    operator = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def _str_(self):
        return f"{self.operator} ({self.source} → {self.destination})"


class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.seat_number} - {'Booked' if self.is_booked else 'Available'}"


class Booking(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    booked_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Booking on {self.bus.operator} - {self.booked_at.strftime('%Y-%m-%d %H:%M')}"

class TravelPackage(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='travel_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=50) 

    def __str__(self):
        return self.title
    


class Tour(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='tour_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=50)
    most_visited = models.BooleanField(default=False) 

    def __str__(self):
        return self.name


class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    otp = models.IntegerField(null=True, blank=True)

    def _str_(self):
        return self.username


class PasswordResetRequest(models.Model):
    email = models.EmailField()
    requested_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def _str_(self):
        return f"Reset requested for {self.email} on {self.requested_at}"






