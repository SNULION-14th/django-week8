from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.request_serializers import SignInRequestSerializer
from tag.models import Tag

from .models import Comment, Like, Post
from .request_serializers import (
    CommentRequestSerializer,
    PostDetailRequestSerializer,
    PostListRequestSerializer,
)
from .serializers import CommentSerializer, PostSerializer

User = get_user_model()


def get_verified_user(author_info):
    if not author_info:
        return None, Response(
            {"detail": "author field missing."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    username = author_info.get("username")
    password = author_info.get("password")
    if not username or not password:
        return None, Response(
            {"detail": "[username, password] fields missing."},
            status=status.HTTP_400_BAD_REQUEST,
        )

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
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create post",
        description="Create a post with optional tags.",
        request=PostListRequestSerializer,
        responses={201: PostSerializer, 400: "Bad Request", 404: "Not Found"},
    )
    def post(self, request):
        author, error_response = get_verified_user(request.data.get("author"))
        if error_response:
            return error_response

        title = request.data.get("title")
        content = request.data.get("content")
        if not title or not content:
            return Response(
                {"detail": "[title, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        post = Post.objects.create(title=title, content=content, author=author)
        set_post_tags(post, request.data.get("tags"))

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostDetailView(APIView):
    @extend_schema(
        summary="Post detail",
        description="Get one post.",
        responses={200: PostSerializer, 404: "Not Found"},
    )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update post",
        description="Update a post. Only the author can update it.",
        request=PostDetailRequestSerializer,
        responses={
            200: PostSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def put(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        author, error_response = get_verified_user(request.data.get("author"))
        if error_response:
            return error_response

        if post.author != author:
            return Response(
                {"detail": "You are not the author of this post."},
                status=status.HTTP_403_FORBIDDEN,
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
        post.save()
        set_post_tags(post, request.data.get("tags"))

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete post",
        description="Delete a post. Only the author can delete it.",
        request=SignInRequestSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

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
        responses={200: CommentSerializer(many=True), 404: "Not Found"},
    )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        comments = post.comments.all().order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create comment",
        description="Create a comment on a post.",
        request=CommentRequestSerializer,
        responses={201: CommentSerializer, 400: "Bad Request", 404: "Not Found"},
    )
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        author, error_response = get_verified_user(request.data.get("author"))
        if error_response:
            return error_response

        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "content field missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment = Comment.objects.create(post=post, author=author, content=content)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(APIView):
    @extend_schema(
        summary="Comment detail",
        description="Get one comment.",
        responses={200: CommentSerializer, 404: "Not Found"},
    )
    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update comment",
        description="Update a comment. Only the author can update it.",
        request=CommentRequestSerializer,
        responses={
            200: CommentSerializer,
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        author, error_response = get_verified_user(request.data.get("author"))
        if error_response:
            return error_response

        if comment.author != author:
            return Response(
                {"detail": "You are not the author of this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        content = request.data.get("content")
        if not content:
            return Response(
                {"detail": "content field missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment.content = content
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Delete comment",
        description="Delete a comment. Only the author can delete it.",
        request=SignInRequestSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found",
        },
    )
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

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
        responses={200: PostSerializer, 400: "Bad Request", 404: "Not Found"},
    )
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        author, error_response = get_verified_user(request.data)
        if error_response:
            return error_response

        like = Like.objects.filter(user=author, post=post).first()
        if like:
            like.delete()
        else:
            Like.objects.create(user=author, post=post)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
