from django.db import models
from account.models import Account
from blog.models import Blog
from datetime import datetime, timedelta
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


class ReactBlog(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    like = models.BooleanField(default=False, null=True)
    dislike = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return str(self.id)

@receiver(pre_save, sender=ReactBlog)
def save_react_blog_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)


class ReactNumberOnBlog(models.Model):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE, null=True)
    number_of_likes = models.PositiveBigIntegerField(default=0, null=True)
    number_of_dislikes = models.PositiveBigIntegerField(default=0, null=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return str(self.id)

@receiver(pre_save, sender=ReactNumberOnBlog)
def save_react_number_on_blog_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)


class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return str(self.id)

@receiver(pre_save, sender=Comment)
def save_comment_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)


class Reply(models.Model):
    sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, related_name="sender")
    receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, related_name="receiver")
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, related_name="comment")
    message = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return str(self.id)

@receiver(pre_save, sender=Reply)
def save_reply_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)
