from django.contrib import admin

from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at")

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "category", "main_image", "created_at")