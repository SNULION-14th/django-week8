from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from .request_serializers import PostListRequestSerializer, PostDetailRequestSerializer

from django.contrib.auth import get_user_model
from tag.models import Tag
from account.request_serializers import SignInRequestSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

class PostListView(APIView):
    @extend_schema(
        summary="게시글 목록 조회",
        description="DB에 저장된 모든 게시글의 목록 조회",
        responses={
            200:PostSerializer(many=True),
            404:"Not Found",
            400:"Bad Request",
        },
    )
    def get(self, request):
        posts = Post.objects.all() #모든 Post를 가져와라
        #아래가 역직렬화
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    @extend_schema(
        summary="새 게시글 작성",
        description="제목과 내용을 입력받아 새로운 게시글을 생성",
        request=PostListRequestSerializer,
        responses={201: PostSerializer,
                   404:"Not Found",
                   400:"Bad Request",
                   },
    )
    def post(self, request):
        title = request.data.get('title')
        content = request.data.get('content')
        tag_contents = request.data.get("tags")
        author_info = request.data.get("author")
        if not author_info:
            return Response({"detail":"author field missing."}, status=status.HTTP_400_BAD_REQUEST),
        username = author_info.get("username")
        password = author_info.get("password")
        
        if not username or not password:
            return Response(
                {"detail: ""[username, password] fields missing in author"}, status = status.HTTP_400_BAD_REQUEST,
            )

        if not title or not content:
            return Response({"detail":"[title,. content] fields missing."}, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail":"Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            post = Post.objects.create(title=title, content=content, author=author)
        
        except:
            return Response(
                {"detail": "User Not Found."}, status = status.HTTP_404_NOT_FOUND
            )
        
        if tag_contents is not None:
            for tag_content in tag_contents:
                if not Tag.objects.filter(content=tag_content).exists():
                    post.tags.create(content=tag_content)
                else:
                    post.tags.add(Tag.objects.get(content=tag_content))

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PostDetailView(APIView):
    @extend_schema(
        summary="게시글 상세 조회",
        description="게시글 1개의 상세 정보 조회",
        responses={200: PostSerializer,
                   400: "Bad Request",},
    )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail":"Not found."}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="게시글 삭제",
        description="게시글을 삭제합니다.",
        responses={204: "No Content",
                   404: "Not Found",
                   400: "Bad Request",},
    )
    def delete(self,request,post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail":"Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        author_info = request.data
        if not author_info:
            return Response(
                {"detail": "author field missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if post.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except:
            return Response(
                {"detail":"User Not Found."},
                status = status.HTTP_404_NOT_FOUND
            )
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        summary="게시글 수정",
        description="게시글을 수정합니다.",
        request=PostDetailRequestSerializer,
        responses={200: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"deatil": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
    
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if post.author != author:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status = status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND,
            )

        title = request.data.get("title")
        content = request.data.get("content")
        if not title or not content:
            return Response(
                {"detail": "[title, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        post.title = title
        post.content = content

        tag_contents = request.data.get("tags")
        if tag_contents is not None:
            post.tags.clear()
            for tag_content in tag_contents:
                if not Tag.objects.filter(content=tag_content).exists():
                    post.tags.create(content=tag_content)
                else:
                    post.tags.add(Tag.objects.get(content=tag_content))
        post.save()
        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)
