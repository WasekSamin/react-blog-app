from django.contrib import admin

from .models import *

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "created_at")
