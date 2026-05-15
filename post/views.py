# ./post/views.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# 수정
from .models import Post, Like, University, Interest, Question
from .serializers import PostSerializer, UniversitySerializer, InterestSerializer, QuestionSerializer
from .request_serializers import PostListRequestSerializer, PostDetailRequestSerializer

from django.contrib.auth import get_user_model
from tag.models import Tag
from account.request_serializers import SignInRequestSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

class PostListView(APIView):
    @extend_schema(
        summary="게시글 목록 조회",
        description="게시글 목록을 조회합니다.",
        responses={
            200: PostSerializer(many=True),
            404: "Not Found",
            400: "Bad Request",
        },
    )
    def get(self, request): 
        posts = Post.objects.all() # Post를 다 가져와라
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @extend_schema(
        summary="게시글 생성",
        description="게시글을 생성합니다.",
        request=PostListRequestSerializer,
        responses={201: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request):
        title = request.data.get("title")
        content = request.data.get("content")
        tag_contents = request.data.get("tags")
        author_info = request.data.get("author")
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing in author"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not title or not content:
            return Response(
                {"detail": "[title, content] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            post = Post.objects.create(title=title, content=content, author=author)
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
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
        description="게시글 1개의 상세 정보를 조회합니다.",
        responses={200: PostSerializer, 400: "Bad Request"},
    )
    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(instance=post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="게시글 삭제",
        description="게시글을 삭제합니다.",
        request=SignInRequestSerializer,
        responses={204: "No Content", 404: "Not Found", 400: "Bad Request"},
    )
    def delete(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post Not found."}, status=status.HTTP_404_NOT_FOUND
            )

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
                status=status.HTTP_400_BAD_REQUEST,
            )
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
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
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
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
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
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
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


class LikeView(APIView):
    @extend_schema(
        summary="좋아요 토글",
        description="좋아요를 토글합니다. 이미 좋아요가 눌려있으면 취소합니다.",
        request=SignInRequestSerializer,
        responses={200: PostSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def post(self, request, post_id):

        ### 1 ###
        try:
            post = Post.objects.get(id=post_id)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        author_info = request.data
        if not author_info:
            return Response(
                {"detail": "author field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = author_info.get("username")
        password = author_info.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ### 2 ###
        try:
            author = User.objects.get(username=username)
            if not author.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        ### 3 ###
        is_liked = post.like_set.filter(user=author).count() > 0

        ### 4 ###
        if is_liked == True:
            post.like_set.get(user=author).delete()
            print("좋아요 취소")
        else:
            Like.objects.create(user=author, post=post)
            print("좋아요 누름")

        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UniversityListView(APIView):
    def get(self, request):
        universities = University.objects.all()
        serializer = UniversitySerializer(universities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
            request=UniversitySerializer,
            responses={201: UniversitySerializer, 400: "Bad Request"},
    )

    def post(self, request):
        serializer = UniversitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UniversityDetailView(APIView):
    def get(self, request, university_id):
        university = University.objects.get(id=university_id)
        serializer = UniversitySerializer(university)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=UniversitySerializer,
        responses={200: UniversitySerializer, 404: "Not Found", 400: "Bad Request"},
    )

    def put(self, request, university_id):
        university = University.objects.get(id=university_id)
        serializer = UniversitySerializer(university, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, university_id):
        university = University.objects.get(id=university_id)
        university.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class InterestListView(APIView):
    def get(self, request):
        interests = Interest.objects.all()
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=InterestSerializer,
        responses={201: InterestSerializer, 400: "Bad Request"},
    )

    def post(self, request):
        serializer = InterestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InterestDetailView(APIView):
    def get(self, request, interest_id):
        interest = Interest.objects.get(id=interest_id)
        serializer = InterestSerializer(interest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=InterestSerializer,
        responses={200: InterestSerializer, 404: "Not Found", 400: "Bad Request"},
    )

    def put(self, request, interest_id):
        interest = Interest.objects.get(id=interest_id)
        serializer = InterestSerializer(interest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, interest_id):
        interest = Interest.objects.get(id=interest_id)
        interest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=QuestionSerializer,
        responses={201: QuestionSerializer, 400: "Bad Request"},
    )

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestionDetailView(APIView):
    def get(self, request, question_id):
        question = Question.objects.get(id=question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=QuestionSerializer,
        responses={200: QuestionSerializer, 404: "Not Found", 400: "Bad Request"},
    )

    def put(self, request, question_id):
        question = Question.objects.get(id=question_id)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        question = Question.objects.get(id=question_id)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)