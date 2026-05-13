from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UserProfile, Stock, Recommendation, Reason, Bookmark
from .serializers import UserProfileSerializer, StockSerializer, RecommendationSerializer, ReasonSerializer, BookmarkSerializer

from drf_spectacular.utils import extend_schema

class UserProfileListView(APIView):
    @extend_schema(
        tags=['Users'],
        summary="유저 전체 목록 조회",
        responses={200: UserProfileSerializer(many=True)}
    )
    def get(self, request):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Users'],
        summary="새로운 유저 생성",
        request=UserProfileSerializer,
        responses={201: UserProfileSerializer, 400: dict}
    )
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileDetailView(APIView):
    @extend_schema(
        tags=['Users'],
        summary="특정 유저 상세 조회",
        responses={200: UserProfileSerializer, 404: dict}
    )
    def get(self, request, pk):
        try:
            user = UserProfile.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=['Users'],
        summary="특정 유저 정보 수정",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer, 400: dict, 404: dict}
    )
    def put(self, request, pk):
        try:
            user = UserProfile.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        tags=['Users'],
        summary="특정 유저 삭제",
        responses={204: None, 404: dict}
    )
    def delete(self, request, pk):
        try:
            user = UserProfile.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class StockListView(APIView):
    @extend_schema(
        tags=['Stocks'],
        summary="주식 전체 목록 조회",
        responses={200: StockSerializer(many=True)}
    )
    def get(self, request):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Stocks'],
        summary="새로운 주식 데이터 생성",
        request=StockSerializer,
        responses={201: StockSerializer, 400: dict}
    )
    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockDetailView(APIView):
    @extend_schema(
        tags=['Stocks'],
        summary="특정 주식 상세 조회",
        responses={200: StockSerializer, 404: dict}
    )
    def get(self, request, pk):
        try:
            stock = Stock.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=['Stocks'],
        summary="특정 주식 정보 수정",
        request=StockSerializer,
        responses={200: StockSerializer, 400: dict, 404: dict}
    )
    def put(self, request, pk):
        try:
            stock = Stock.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        tags=['Stocks'],
        summary="특정 주식 삭제",
        responses={204: None, 404: dict}
    )
    def delete(self, request, pk):
        try:
            stock = Stock.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RecommendationListView(APIView):
    @extend_schema(
        tags=['Recommendations'],
        summary="추천 레포트 전체 목록 조회",
        responses={200: RecommendationSerializer(many=True)}
    )
    def get(self, request):
        recommendations = Recommendation.objects.all()
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Recommendations'],
        summary="새로운 추천 레포트 생성",
        request=RecommendationSerializer,
        responses={201: RecommendationSerializer, 400: dict}
    )
    def post(self, request):
        serializer = RecommendationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationDetailView(APIView):
    @extend_schema(
        tags=['Recommendations'],
        summary="특정 추천 레포트 상세 조회",
        responses={200: RecommendationSerializer, 404: dict}
    )
    def get(self, request, pk):
        try:
            recommendation = Recommendation.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecommendationSerializer(recommendation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=['Recommendations'],
        summary="특정 추천 레포트 정보 수정",
        request=RecommendationSerializer,
        responses={200: RecommendationSerializer, 400: dict, 404: dict}
    )
    def put(self, request, pk):
        try:
            recommendation = Recommendation.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecommendationSerializer(recommendation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        tags=['Recommendations'],
        summary="특정 추천 레포트 삭제",
        responses={204: None, 404: dict}
    )
    def delete(self, request, pk):
        try:
            recommendation = Recommendation.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        recommendation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReasonListView(APIView):
    @extend_schema(
        tags=['Reasons'],
        summary="추천 상세 근거 전체 목록 조회",
        responses={200: ReasonSerializer(many=True)}
    )
    def get(self, request):
        reasons = Reason.objects.all()
        serializer = ReasonSerializer(reasons, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Reasons'],
        summary="새로운 추천 상세 근거 생성",
        request=ReasonSerializer,
        responses={201: ReasonSerializer, 400: dict}
    )
    def post(self, request):
        serializer = ReasonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReasonDetailView(APIView):
    @extend_schema(
        tags=['Reasons'],
        summary="특정 추천 근거 상세 조회",
        responses={200: ReasonSerializer, 404: dict}
    )
    def get(self, request, pk):
        try:
            reason = Reason.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReasonSerializer(reason)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=['Reasons'],
        summary="특정 추천 근거 정보 수정",
        request=ReasonSerializer,
        responses={200: ReasonSerializer, 400: dict, 404: dict}
    )
    def put(self, request, pk):
        try:
            reason = Reason.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReasonSerializer(reason, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        tags=['Reasons'],
        summary="특정 추천 근거 삭제",
        responses={204: None, 404: dict}
    )
    def delete(self, request, pk):
        try:
            reason = Reason.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        reason.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BookmarkListView(APIView):
    @extend_schema(
        tags=['Bookmarks'],
        summary="북마크 전체 목록 조회",
        responses={200: BookmarkSerializer(many=True)}
    )
    def get(self, request):
        bookmarks = Bookmark.objects.all()
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Bookmarks'],
        summary="새로운 북마크 생성",
        request=BookmarkSerializer,
        responses={201: BookmarkSerializer, 400: dict}
    )
    def post(self, request):
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookmarkDetailView(APIView):
    @extend_schema(
        tags=['Bookmarks'],
        summary="특정 북마크 상세 조회",
        responses={200: BookmarkSerializer, 404: dict}
    )
    def get(self, request, pk):
        try:
            bookmark = Bookmark.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        tags=['Bookmarks'],
        summary="특정 북마크 정보 수정",
        request=BookmarkSerializer,
        responses={200: BookmarkSerializer, 400: dict, 404: dict}
    )
    def put(self, request, pk):
        try:
            bookmark = Bookmark.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookmarkSerializer(bookmark, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        tags=['Bookmarks'],
        summary="특정 북마크 삭제",
        responses={204: None, 404: dict}
    )
    def delete(self, request, pk):
        try:
            bookmark = Bookmark.objects.get(pk=pk)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)