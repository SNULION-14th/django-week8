from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Crew, CrewGoal
from .serializers import CrewSerializer, CrewGoalSerializer
from drf_spectacular.utils import extend_schema
# Create your views here.
class CrewListView(APIView):
  @extend_schema(
      summary="크루 조회",
      description="DB에 저장된 모든 크루의 목록을 조회합니다.",
      responses={200: CrewSerializer(many=True)}
  )
  def get(self,request):
    crews = Crew.objects.all()
    serializer = CrewSerializer(crews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
  
  @extend_schema(
        summary="새 크루 등록",
        description="이름과 목표를 입력받아 새로운 크루를 생성합니다.",
        request=CrewSerializer,
        responses={201: CrewSerializer}
    )
  def post(self, request):
    name = request.data.get("name")
    content = request.data.get("content")
    if not name or not content:
      return Response({"detail":"[name,content] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
    crew = Crew.objects.create(name=name, content=content)
    serializer = CrewSerializer(crew)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  

class CrewDetailView(APIView):
  @extend_schema(
      summary="크루 상세 조회",
      description="크루 1개의 상세 정보를 조회합니다.",
      responses={200: CrewSerializer}
  )
  def get(self, request, crew_id):
    try:
      crew = Crew.objects.get(id=crew_id)
    except:
      return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = CrewSerializer(crew)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
        summary="크루 삭제",
        description="크루를 삭제합니다.",
        responses={204: None} # 204는 돌아오는 데이터가 없으므로 None
    )
  def delete(self, request, crew_id):
    try:
      crew = Crew.objects.get(id=crew_id)
    except:
      return Response({"detail": "Not Found"}, status = status.HTTP_404_NOT_FOUND)
    crew.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
class CrewGoalListView(APIView):
    @extend_schema(
        summary="크루 목표 전체 조회",
        description="DB에 저장된 모든 크루 목표를 조회합니다.",
        responses={200: CrewGoalSerializer(many=True)}
    )
    def get(self, request):
        goals = CrewGoal.objects.all().order_by("-created_at")
        serializer = CrewGoalSerializer(goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="크루 목표 생성",
        description="크루의 운동 목표와 목표 달성 시 기부 금액을 생성합니다.",
        request=CrewGoalSerializer,
        responses={201: CrewGoalSerializer}
    )
    def post(self, request):
        serializer = CrewGoalSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrewGoalDetailView(APIView):
    def get_object(self, goal_id):
        try:
            return CrewGoal.objects.get(id=goal_id)
        except CrewGoal.DoesNotExist:
            return None

    @extend_schema(
        summary="크루 목표 상세 조회",
        description="크루 목표 1개의 상세 정보를 조회합니다.",
        responses={200: CrewGoalSerializer}
    )
    def get(self, request, goal_id):
        goal = self.get_object(goal_id)

        if goal is None:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CrewGoalSerializer(goal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="크루 목표 삭제",
        description="크루 목표를 삭제합니다.",
        responses={204: None}
    )
    def delete(self, request, goal_id):
        goal = self.get_object(goal_id)

        if goal is None:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)