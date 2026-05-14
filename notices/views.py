from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from utils.auth import authorize_user
from .models import Notice, Source, SourceSubscription, InboxNotice
from .serializers import NoticeSerializer, SourceSerializer, SourceSubscriptionSerializer, InboxNoticeSerializer
from .request_serializers import SourceSubscriptionListRequestSerializer, SourceSubscriptionDetailRequestSerializer

User = get_user_model()


class NoticeListView(APIView):
  @extend_schema(
    summary="공지 목록 조회",
    description="공지 목록을 조회합니다.",
    responses={
      200: NoticeSerializer(many=True),
      404: "Not Found",
      400: "Bad Request",
    },
  )
  def get(self, request):
    notices = Notice.objects.all()
    serializer = NoticeSerializer(notices, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class NoticeDetailView(APIView):
  @extend_schema(
    summary="공지 상세 조회",
    description="공지 1개의 상세 정보를 조회합니다.",
    responses={
      200: NoticeSerializer,
      400: "Bad Request"
    },
  )
  def get(self, request, notice_id):
      try:
        notice = Notice.objects.get(id=notice_id)
      except:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

      serializer = NoticeSerializer(instance=notice)
      return Response(serializer.data, status=status.HTTP_200_OK)


class SourceListView(APIView):
  @extend_schema(
    summary="게시판 목록 조회",
    description="게시판 목록을 조회합니다.",
    responses={
      200: SourceSerializer(many=True),
      404: "Not Found",
      400: "Bad Request",
    },
  )
  def get(self, request):
    sources = Source.objects.all()
    serializer = SourceSerializer(sources, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class SourceDetailView(APIView):
  @extend_schema(
    summary="게시판 상세 조회",
    description="게시판 1개의 상세 정보를 조회합니다.",
    responses={
      200: SourceSerializer,
      400: "Bad Request"
    },
  )
  def get(self, request, source_id):
      try:
        source = Source.objects.get(id=source_id)
      except:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

      serializer = SourceSerializer(instance=source)
      return Response(serializer.data, status=status.HTTP_200_OK)


class SourceSubscriptionListView(APIView):
  @extend_schema(
    summary="구독 중인 게시판 목록 조회",
    description="구독 중인 게시판 목록을 조회합니다.",
    responses={
      200: SourceSubscriptionSerializer(many=True),
      404: "Not Found",
      400: "Bad Request",
    },
  )
  def get(self, request, user_id):
    subscription_sources = SourceSubscription.objects.filter(user=user_id)
    serializer = SourceSubscriptionSerializer(subscription_sources, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @extend_schema(
    summary="게시판 구독 생성",
    description="게시판 구독을 생성합니다.",
    request=SourceSubscriptionListRequestSerializer,
    responses={
      201: SourceSubscriptionSerializer,
      404: "Not Found",
      400: "Bad Request"
    },
  )
  def post(self, request, user_id):
    user_info = request.data.get("user")
    name = request.data.get("source_name")
    url = request.data.get("source_url")
    crawl_interval_minutes = request.data.get("source_crawl_interval_minutes")

    auth = authorize_user(User, user_info)
    if not auth.is_auth:
      return auth.response
    if user_id != auth.user.id:
      return Response(
        {"detail": "User unmatched"},
        status=status.HTTP_400_BAD_REQUEST,
      )
    if crawl_interval_minutes < 60:
      return Response(
        {"detail": "crawl interval must be more than 60 minutes"},
        status=status.HTTP_400_BAD_REQUEST,
      )
    
    if not (name and url):
      return Response(
        {"detail": "[source_name, source_url] fields missing."},
        status=status.HTTP_400_BAD_REQUEST,
      )
    
    try:
      source = Source.objects.get(name=name, url=url)
      if SourceSubscription.objects.filter(user=user_id, source=source).exists():
          return Response(
          {"detail": "The source already subscribed"},
          status=status.HTTP_400_BAD_REQUEST,
        )

      source.crawl_interval_minutes = min(crawl_interval_minutes, source.crawl_interval_minutes)
      source.save()
      auth.user.subscription_sources.add(source)
    except:
      source = auth.user.subscription_sources.create(name=name, url=url, crawl_interval_minutes=crawl_interval_minutes)
    
    serializer = SourceSubscriptionSerializer(SourceSubscription.objects.get(user=user_id, source=source))
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class SourceSubscriptionDetailView(APIView):
  @extend_schema(
    summary="게시판 구독 상세 조회",
    description="게시판 구독 1개의 상세 정보를 조회합니다.",
    responses={
      200: SourceSubscriptionSerializer,
      400: "Bad Request"
    },
  )
  def get(self, request, user_id, subscription_id):
    try:
      subscription_source = SourceSubscription.objects.get(user=user_id, id=subscription_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = SourceSubscriptionSerializer(instance=subscription_source)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
    summary="게시판 구독 삭제",
    description="게시판 구독을 삭제합니다.",
    responses={
      204: "No Content",
      404: "Not Found",
      400: "Bad Request"
    },
  )
  def delete(self, request, user_id, subscription_id):
    try:
      subscription_source = SourceSubscription.objects.get(user=user_id, id=subscription_id)
    except:
      return Response(
        {"detail": "Subscription Not found."}, status=status.HTTP_404_NOT_FOUND
      )

    subscription_source.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class InboxNoticeListView(APIView):
  pass

class InboxNoticeDetailView(APIView):
  pass
