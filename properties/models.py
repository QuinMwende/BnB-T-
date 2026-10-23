from django.db import models
from users.models import User
# Create your models here.

class Property(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    location = models.CharField(max_length=255)

    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    max_guests = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title