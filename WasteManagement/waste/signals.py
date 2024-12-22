# waste/signals.py
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import WasteReport
from django.db.models import Count

@receiver(post_delete, sender=WasteReport)
def sync_points_on_delete(sender, instance, **kwargs):
    """
    Automatically sync points whenever a report is deleted
    """
    sync_user_points(instance.user)

@receiver(post_save, sender=WasteReport)
def sync_points_on_save(sender, instance, **kwargs):
    """
    Automatically sync points whenever a report is saved
    """
    sync_user_points(instance.user)