from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# Custom User Manager
class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model to handle email-based authentication.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractUser):
    """
    Custom user model where email is the unique identifier instead of username.
    """
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    phone_number = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Phone Number'))
    points = models.IntegerField(default=0, verbose_name=_('Points'))

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # No additional fields are required

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Waste Report Model
class WasteReport(models.Model):
    """
    Model to store waste report submissions.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='waste_reports')
    photo = models.ImageField(upload_to='waste_photos/', verbose_name=_('Photo'))
    photo_hash = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Photo Hash'))
    location = models.CharField(max_length=255, verbose_name=_('Location'))
    waste_type = models.CharField(max_length=50, verbose_name=_('Waste Type'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='low',
        verbose_name=_('Priority')
    )
    contact_information = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Contact Information'))
    nearby_landmarks = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Nearby Landmarks'))
    latitude = models.FloatField(null=True, blank=True, verbose_name=_('Latitude'))
    longitude = models.FloatField(null=True, blank=True, verbose_name=_('Longitude'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return f"{self.user.email} - {self.waste_type}"
