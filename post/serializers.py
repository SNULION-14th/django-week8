# post/serializers.py

from rest_framework.serializers import ModelSerializer
from tag.serializers import TagSerializer
from .models import Post, University, Interest, Question

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class UniversitySerializer(ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"


class InterestSerializer(ModelSerializer):
    class Meta:
        model = Interest
        fields = "__all__"


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"