from enum import unique
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta

class Subscribe(models.Model):
    email = models.EmailField(null=True, unique=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.email

@receiver(pre_save, sender=Subscribe)
def subscribe_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)
