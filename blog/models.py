from django.db import models
from datetime import datetime, timedelta
from PIL import Image
from account.models import Account
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings

from .nudity_detection import load_model, classify, IMAGE_DIM


# Create your models here.


class Category(models.Model):
    # Health, Gaming, Politics, Travelling, Religion, Science, Life Style, Food
    title = models.CharField(max_length=120, null=True, unique=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Category)
def save_category_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)


class Tag(models.Model):
    title = models.CharField(max_length=120, null=True, unique=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Tag)
def save_tag_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)


class Blog(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=120, null=True)
    main_image = models.ImageField(
        upload_to="blog/images", null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    post_text = models.TextField(null=True)
    created_at = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return str(self.id)

    def save(self):
        super(Blog, self).save()

        if not self.main_image:
            return

        img_path = self.main_image.path
        model = load_model(
            "static/nudity_detection_model/Nudity-Detection-Model.h5")
        image_preds = classify(model, img_path, IMAGE_DIM)
        if (image_preds[img_path]["porn"] >= image_preds[img_path]["drawings"] and image_preds[img_path]["porn"] >= image_preds[img_path]["neutral"] and image_preds[img_path]["porn"] >= image_preds[img_path]["sexy"] and image_preds[img_path]["porn"] >= image_preds[img_path]["hentai"]) or \
                (image_preds[img_path]["hentai"] >= image_preds[img_path]["drawings"] and image_preds[img_path]["hentai"] >= image_preds[img_path]["neutral"] and image_preds[img_path]["hentai"] >= image_preds[img_path]["sexy"] and image_preds[img_path]["hentai"] >= image_preds[img_path]["porn"]):
            # print("It is a nude image!")
            settings.NUDE_DETECTED = True
        # print(json.dumps(image_preds, indent=2), '\n')

        image = Image.open(self.main_image)
        size = (800, 450)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.main_image.path)


@receiver(pre_save, sender=Blog)
def save_blog_created_time(sender, instance, **kwargs):
    instance.created_at = instance.created_at + timedelta(hours=8)
