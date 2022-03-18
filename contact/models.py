from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime, timedelta


class Contact(models.Model):
    email = models.EmailField(null=True)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return str(self.id)


@receiver(pre_save, sender=Contact)
def save_contact_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)
