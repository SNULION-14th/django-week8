from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from utils.auth import authorize_user
from .models import Notice, Source, SourceSubscription, InboxNotice
from .serializers import NoticeSerializer, SourceSerializer, SourceSubscriptionSerializer, InboxNoticeSerializer


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
  pass

class SourceDetailView(APIView):
  pass

class SourceSubscriptionListView(APIView):
  pass

class InboxNoticeListView(APIView):
  pass

class InboxNoticeDetailView(APIView):
  pass
