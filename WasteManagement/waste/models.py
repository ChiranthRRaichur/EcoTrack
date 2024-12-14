from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class WasteReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
        return self.waste_type




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    points = models.IntegerField(default=0)  # Add a field for user points

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# Unused models commented out
# class WasteIssue(models.Model):
#     ISSUE_TYPES = [
#         ('General', 'General'),
#         ('Electronic', 'Electronic'),
#         ('Hazardous', 'Hazardous'),
#     ]
# 
#     issue_type = models.CharField(max_length=20, choices=ISSUE_TYPES)
#     description = models.TextField()
#     location = models.CharField(max_length=100)
#     status = models.CharField(max_length=20, default='Pending')
#     reported_date = models.DateTimeField(default=timezone.now)
#     reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues', null=True)
# 
#     def __str__(self):
#         return f"{self.issue_type} - {self.location}"

# class PickupRequest(models.Model):
#     item_description = models.TextField()
#     location = models.CharField(max_length=100)
#     status = models.CharField(max_length=20, default='Pending')
#     requested_date = models.DateTimeField(default=timezone.now)
#     requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pickups', null=True)
# 
#     def __str__(self):
#         return f"{self.item_description} - {self.location}"

# class UserImage(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='user_images/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
# 
#     def __str__(self):
#         return f"Image uploaded by {self.user.email}"

# class WasteReport(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     photo = models.ImageField(upload_to='waste_photos/')
#     location = models.CharField(max_length=255)
#     waste_type = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
# 
#     def __str__(self):
#         return f"{self.user.email} - {self.waste_type}"
