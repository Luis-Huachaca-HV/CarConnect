# signals.py

from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from .models import Expense, Maintenance

@receiver(post_save, sender=Expense)
def update_maintenance_total_spent(sender, instance, **kwargs):
    maintenance = instance.maintenance
    total_spent = Expense.objects.filter(maintenance=maintenance).aggregate(total=models.Sum('amount'))['total']
    maintenance.total_spent = total_spent
    maintenance.save()
