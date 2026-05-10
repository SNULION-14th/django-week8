from rest_framework.serializers import ModelSerializer
from tag.serializers import TagSerializer
from .models import Post,Like

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = "__all__"

class LikeSerializer(ModelSerializer):
    # 주의: UserIdUsernameSerializer와 PostSerializer가 먼저 정의되어 있어야 합니다
    # user = UserIdUsernameSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['user', 'post', 'created_at']