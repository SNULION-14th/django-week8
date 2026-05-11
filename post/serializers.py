# ./post/serializers.py

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from tag.serializers import TagSerializer
from .models import Post, Log


class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"


class LogSerializer(ModelSerializer):
    user_nickname = serializers.ReadOnlyField(source='user.username')
    exhibition_title = serializers.ReadOnlyField(source='exhibition.title')

    class Meta:
        model = Log
        fields = [
            'log_id',
            'user', 'user_nickname',
            'exhibition', 'exhibition_title',
            'content', 'rating',
            'created_at', 'updated_at',
        ]