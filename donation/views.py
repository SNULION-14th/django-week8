from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Donation
from .serializers import DonationSerializer

# Create your views here.
class DonationListView(APIView):
  @extend_schema(
    summary="기부 기록 전체 조회",
    description="목표 달성으로 생성된 모든 기부 기록을 조회합니다.",
    responses={200: DonationSerializer(many=True)}
  )

  def get(self,request):
    donations = Donation.objects.all().order_by("-created_at")
    serializer = DonationSerializer(donations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class DonationDetailView(APIView):
  def get_object(self, donation_id):
    try: 
      return Donation.objects.get(id=donation_id)
    except Donation.DoesNotExist:
      return None
    
  @extend_schema(
    summary="기부 기록 상세 조회",
    description="기부 기록 1개의 상세 정보를 조회합니다.",
    responses={200: DonationSerializer}
  )

  def get(self, request, donation_id):
    donation = self.get_object(donation_id)

    if donation is None:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    serializer = DonationSerializer(donation)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
    if serializer.is_valid():
       donation = serializer.save()

       if donation.status == "completed" and donation.completed_at is None:
          donation.completed_at = timezone.now()
          donation.save()

       serializer = DonationSerializer(donation)
       return Response(serializer.data, satatus=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  @extend_schema(
     summary="기부 기록 삭제",
      description="기부 기록 1개를 삭제합니다.",
      responses={204: None}
  )
  def delete(self,request,donation_id):
     donation = self.get_object(donation_id)

     if donation is None:
      return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )
      donation.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)