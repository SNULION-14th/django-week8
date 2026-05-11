# post/views.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

# 추가
from drf_spectacular.utils import extend_schema

class PostListView(APIView):
    # GET 메소드에 대한 설명 추가
    @extend_schema(
        summary="게시글 목록 조회",
        description="DB에 저장된 모든 게시글의 목록을 조회합니다.",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request): 
        posts = Post.objects.all() # Post를 다 가져와라
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # POST 메소드에 대한 설명 추가
    @extend_schema(
        summary="새 게시글 작성",
        description="제목과 내용을 입력받아 새로운 게시글을 생성합니다.",
        request=PostSerializer,
        responses={201: PostSerializer}
    )
    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            return Response({"detail": "[title, content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.create(title=title, content=content)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            
class PostDetailView(APIView):
    # GET 메소드에 대한 설명 추가
    @extend_schema(
        summary="게시글 상세 조회",
        description="게시글 1개의 상세 정보를 조회합니다.",
        responses={200: PostSerializer}
    )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        # 수정
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # DELETE 메소드에 대한 설명 추가
    @extend_schema(
        summary="게시글 삭제",
        description="게시글을 삭제합니다.",
        responses={204: None} # 204는 돌아오는 데이터가 없으므로 None
    )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)