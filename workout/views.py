from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import WorkoutRecord
from .serializers import WorkoutRecordSerializer
from .services import check_crew_goal_achievement

class WorkoutRecordListView(APIView):
  @extend_schema(
      summary="운동기록 목록 조회",
      description="DB에 저장된 모든 운동기록의 목록을 조회합니다.",
      responses={200: WorkoutRecordSerializer(many=True)}
  )
  def get(self,request):
    records = WorkoutRecord.objects.all().order_by("-created_at")
    serializer = WorkoutRecordSerializer(records, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
        summary="운동 기록 생성",
        description="사용자, 크루, 운동 종류, 거리, 시간, 날짜를 입력받아 운동 기록을 생성합니다.",
        request=WorkoutRecordSerializer,
        responses={201: WorkoutRecordSerializer}
    )
  def post(self, request):
    serializer = WorkoutRecordSerializer(data=request.data)

    if serializer.is_valid():
      record = serializer.save()

      check_crew_goal_achievement(record.crew)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class WorkoutRecordDetailView(APIView):
  def get_object(self, record_id):
    try:
       return WorkoutRecord.objects.get(id=record_id)
    except WorkoutRecord.DoesNotExist:
      return None
    
  @extend_schema(
    summary="운동 기록 상세 조회",
    description="운동 기록 1개의 상세 정보를 조회합니다.",
    responses={200: WorkoutRecordSerializer}
  )
  def get(self,request, record_id):
    record = self.get_object(record_id)

    if record is None:
      return Response(
        {"detail": "Not found."},
        status=status.HTTP_404_NOT_FOUND
      )
    serializer = WorkoutRecordSerializer(record)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
    summary="운동 기록 수정",
    description="운동 기록 1개의 내용을 수정합니다.",
    request=WorkoutRecordSerializer,
    responses={200: WorkoutRecordSerializer}
  )
  def patch(self,request,record_id):
    record = self.get_object(record_id)

    if record is None:
      return Response(
        {"detail": "Not found."},
        status=status.HTTP_404_NOT_FOUND
      )
    
    serializer = WorkoutRecordSerializer(
            record,
            data=request.data,
            partial=True
    )

    if serializer.is_valid():
      record = serializer.save()

      check_crew_goal_achievement(record.crew)

      return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  @extend_schema(
        summary="운동 기록 삭제",
        description="운동 기록 1개를 삭제합니다.",
        responses={204: None}
    )
  def delete(self, request, record_id):
    record = self.get_object(record_id)
    if record is None:
      return Response(
        {"detail": "Not found."},
        status=status.HTTP_404_NOT_FOUND
        )

    record.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)