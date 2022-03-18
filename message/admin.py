from django.contrib import admin

from .models import *

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "blog", "created_at")

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "comment", "created_at")


@admin.register(ReactBlog)
class ReactBlogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "blog", "like", "dislike", "created_at")

@admin.register(ReactNumberOnBlog)
class ReactNumberOnBlogAdmin(admin.ModelAdmin):
    list_display = ("id", "blog", "number_of_likes", "number_of_dislikes", "created_at")