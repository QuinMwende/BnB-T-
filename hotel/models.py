from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    ROOM_TYPES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
        ('Penthouse', 'Penthouse'),
    ]
    STATUS_CHOICES = [
        ('free', 'Free'),
        ('occupied', 'Occupied'),
        ('cleaning', 'Cleaning'),
    ]
    id = models.CharField(max_length=10, primary_key=True)  # e.g., HS-01
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='free')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    current_guest = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.room_type}"

class Booking(models.Model):
    PAYMENT_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
    ]
    guest_name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.guest_name} in {self.room.id}"
