from django.db import models
from bookings.models import Booking

# Create your models here.
class Payment(models.Model):
    PAYMENT_METHODS = (
        ('mpesa', 'Mpesa'),
        ('card', 'Card'),
    )

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS)

    paid_at = models.DateTimeField(null=True, blank=True)