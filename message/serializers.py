from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        depth = 2


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"
        depth = 3


class ReactBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactBlog
        fields = "__all__"
        depth = 2


class ReactNumberOnBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReactNumberOnBlog
        fields = "__all__"
        depth = 2
