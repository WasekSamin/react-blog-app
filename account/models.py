from django.db import models
from datetime import datetime, timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=120, null=True)
    email = models.EmailField(null=True, unique=True)
    token = models.CharField(max_length=50, null=True, unique=True)
    password = models.CharField(max_length=120, null=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.email

@receiver(pre_save, sender=Account)
def save_account_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)