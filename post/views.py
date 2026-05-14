from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.request_serializers import SignInRequestSerializer
from seminar.serializers import DetailResponseSerializer
from tag.models import Tag

from .models import Comment, Like, Post
from .request_serializers import (
    CommentRequestSerializer,
    PostDetailRequestSerializer,
    PostListRequestSerializer,
)
from .serializers import CommentSerializer, PostSerializer

User = get_user_model()


def post_queryset():
    return Post.objects.select_related("author").prefetch_related("tags", "comments", "like_users")


def get_verified_user(author_info):
    if not author_info:
        return None, Response(
            {"detail": "author field missing."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = SignInRequestSerializer(data=author_info)
    if not serializer.is_valid():
        return None, Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]

    try:
        author = User.objects.get(username=username)
    except User.DoesNotExist:
        return None, Response(
            {"detail": "User not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not author.check_password(password):
        return None, Response(
            {"detail": "Password is incorrect."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return author, None


def set_post_tags(post, tag_contents):
    if tag_contents is None:
        return

    post.tags.clear()
    for tag_content in tag_contents:
        tag, _ = Tag.objects.get_or_create(content=tag_content)
        post.tags.add(tag)


class PostListView(APIView):
    @extend_schema(
        summary="Post list",
        description="Get all posts.",
        responses={200: PostSerializer(many=True)},
    )
    def get(self, request):
        posts = post_queryset().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create post",
        description="Create a post with optional tags.",
        request=PostListRequestSerializer,
        responses={201: PostSerializer, 400: DetailResponseSerializer, 404: DetailResponseSerializer},
    )
    def post(self, request):
        request_serializer = PostListRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        author, error_response = get_verified_user(request_serializer.validated_data.get("author"))
        if error_response:
            return error_response

        post = Post.objects.create(
            title=request_serializer.validated_data["title"],
            content=request_serializer.validated_data["content"],
            author=author,
        )
        set_post_tags(post, request_serializer.validated_data.get("tags"))

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):
    @extend_schema(
        summary="Post detail",
        description="Get one post.",
        responses={200: PostSerializer, 404: DetailResponseSerializer},
    )
    def get(self, request, post_id):
        post = get_object_or_404(post_queryset(), id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update post",
        description="Update a post. Only the author can update it.",
        request=PostDetailRequestSerializer,
        responses={
            200: PostSerializer,
            400: DetailResponseSerializer,
            403: DetailResponseSerializer,
            404: DetailResponseSerializer,
        },
    )
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        request_serializer = PostDetailRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        author, error_response = get_verified_user(request_serializer.validated_data.get("author"))
        if error_response:
            return error_response

        if post.author != author:
            return Response(
                {"detail": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN,
            )

        post.title = request_serializer.validated_data["title"]
        post.content = request_serializer.validated_data["content"]
        post.save()
        set_post_tags(post, request_serializer.validated_data.get("tags"))

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete post",
        description="Delete a post. Only the author can delete it.",
        request=SignInRequestSerializer,
        responses={
            204: OpenApiResponse(description="No Content"),
            400: DetailResponseSerializer,
            403: DetailResponseSerializer,
            404: DetailResponseSerializer,
        },
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        author, error_response = get_verified_user(request.data)
        if error_response:
            return error_response

        if post.author != author:
            return Response(
                {"detail": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN,
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):
    @extend_schema(
        summary="Comment list",
        description="Get comments on a post.",
        responses={200: CommentSerializer(many=True), 404: DetailResponseSerializer},
    )
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.select_related("author").order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create comment",
        description="Create a comment on a post.",
        request=CommentRequestSerializer,
        responses={201: CommentSerializer, 400: DetailResponseSerializer, 404: DetailResponseSerializer},
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        request_serializer = CommentRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        author, error_response = get_verified_user(request_serializer.validated_data.get("author"))
        if error_response:
            return error_response

        comment = Comment.objects.create(
            post=post,
            author=author,
            content=request_serializer.validated_data["content"],
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    @extend_schema(
        summary="Comment detail",
        description="Get one comment.",
        responses={200: CommentSerializer, 404: DetailResponseSerializer},
    )
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment.objects.select_related("author", "post"), id=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update comment",
        description="Update a comment. Only the author can update it.",
        request=CommentRequestSerializer,
        responses={
            200: CommentSerializer,
            400: DetailResponseSerializer,
            403: DetailResponseSerializer,
            404: DetailResponseSerializer,
        },
    )
    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        request_serializer = CommentRequestSerializer(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        author, error_response = get_verified_user(request_serializer.validated_data.get("author"))
        if error_response:
            return error_response

        if comment.author != author:
            return Response(
                {"detail": "You are not the author of this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.content = request_serializer.validated_data["content"]
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete comment",
        description="Delete a comment. Only the author can delete it.",
        request=SignInRequestSerializer,
        responses={
            204: OpenApiResponse(description="No Content"),
            400: DetailResponseSerializer,
            403: DetailResponseSerializer,
            404: DetailResponseSerializer,
        },
    )
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        author, error_response = get_verified_user(request.data)
        if error_response:
            return error_response

        if comment.author != author:
            return Response(
                {"detail": "You are not the author of this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeView(APIView):
    @extend_schema(
        summary="Toggle like",
        description="Like a post. If already liked, cancel the like.",
        request=SignInRequestSerializer,
        responses={200: PostSerializer, 400: DetailResponseSerializer, 404: DetailResponseSerializer},
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        author, error_response = get_verified_user(request.data)
        if error_response:
            return error_response

        like = Like.objects.filter(user=author, post=post).first()
        if like:
            like.delete()
        else:
            Like.objects.create(user=author, post=post)

        serializer = PostSerializer(get_object_or_404(post_queryset(), id=post_id))
        return Response(serializer.data, status=status.HTTP_200_OK)
