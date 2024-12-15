from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class WasteReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='waste_reports')
    photo = models.ImageField(upload_to='waste_photos/')  # Make sure this field exists
    location = models.CharField(max_length=255)
    waste_type = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='low')
    contact_information = models.CharField(max_length=255, blank=True, null=True)
    nearby_landmarks = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically generated timestamp

    def __str__(self):
        return f"{self.user.email} - {self.waste_type}"




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    points = models.IntegerField(default=0)  # Add a field for user points

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
