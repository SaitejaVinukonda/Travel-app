from django.db import models

class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    otp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

class PasswordResetRequest(models.Model):
    email = models.EmailField()
    requested_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset requested for {self.email} on {self.requested_at}"

class Bus(models.Model):
    operator = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.operator} ({self.source} → {self.destination})"

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} - {'Booked' if self.is_booked else 'Available'}"

class Booking(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seats = models.ManyToManyField(Seat)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)

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
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hotel_images/')
    description = models.TextField()

    def __str__(self):
        return self.name

class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"

class HotelBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.room.hotel.name}"
