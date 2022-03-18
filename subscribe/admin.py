from django.contrib import admin

from .models import *

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "created_at")
