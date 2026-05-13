from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Task, Task_history, Scheduled_task
from .serializers import TaskSerializer, TaskHistorySerializer, ScheduledTaskSerializer
from drf_spectacular.utils import extend_schema

# 모든 할일(Task) 목록 불러오기
class TaskListView(APIView):
  @extend_schema(
        summary="할일(Task) 목록 조회",
        description="DB에 저장된 모든 할일의 목록을 조회합니다.",
        responses={200: TaskSerializer(many=True)}
    )
  def get(self, request): 
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
        summary="새로운 할일(Task) 등록",
        description="이름과 카테고리 등을 입력받아 새로운 할일을 등록합니다.",
        request=TaskSerializer,
        responses={201: TaskSerializer}
    )
  def post(self, request):
    title = request.data.get('title')
    category = request.data.get('category')
    priority = request.data.get('priority')
    deadline = request.data.get('deadline')
    estimated_duration = request.data.get('estimated_duration')
    task_status = request.data.get('status')
    if not title or not category or not priority or not deadline or not estimated_duration:
      return Response({"detail": "[title, category, priority, deadline, estimated_duration] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
    task = Task.objects.create(
                            title=title, 
                            category=category,
                            priority=priority,
                            deadline=deadline,
                            estimated_duration=estimated_duration,
                            status=task_status)
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class TaskSingleView(APIView):
  @extend_schema(
        summary="할일(Task) 상세 조회",
        description="할일 1개의 상세 정보를 조회합니다.",
        responses={200: TaskSerializer}
    )
  def get(self, request, task_id):
    try:
      task = Task.objects.get(id=task_id)
    except:
      return Response({"single": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
        summary="할일(Task) 삭제",
        description="할일을 삭제합니다.",
        responses={204: None} # 204는 돌아오는 데이터가 없으므로 None
    )
  def delete(self, request, task_id):
    try:
      task = Task.objects.get(id=task_id)
    except:
      return Response({"single": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
class TaskHistoryView(APIView):
  @extend_schema(
        summary="완료된 할일 기록",
        description="소요 시간 등과 함께 완료된 할일을 기록합니다.",
        request=TaskHistorySerializer,
        responses={201: TaskHistorySerializer}
    )
  def post(self, request):
    planned_duration = request.data.get('planned_duration')
    actual_duration = request.data.get('actual_duration')
    completed_at = request.data.get('completed_at')
    task_id = request.data.get('task_id')
    task = Task.objects.get(id=task_id)
    if not planned_duration or not actual_duration or not completed_at:
      return Response({"detail": "[planned_duration, actual_duration, completed_at] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
    task_history = Task_history.objects.create(
                            planned_duration=planned_duration,
                            actual_duration=actual_duration,
                            completed_at=completed_at,
                            task_id=task)
    serializer = TaskHistorySerializer(task_history)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class TaskHistorySingleView(APIView):
  @extend_schema(
        summary="완료된 할일 상세 조회",
        description="완료된 할일 1개의 상세 정보를 조회합니다.",
        responses={200: TaskHistorySerializer}
    )
  def get(self, request, history_id):
    try:
      task = Task_history.objects.get(id=history_id)
    except:
      return Response({"single": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskHistorySerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
        summary="완료된 할일 삭제",
        description="완료된 할일을 삭제합니다.",
        responses={204: None}
    )
  def delete(self, request, history_id):
    try:
      task =  Task_history.objects.get(id=history_id)
    except:
      return Response({"single": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  

class ScheduledTaskView(APIView):
  @extend_schema(
        summary="새로운 일정 배정",
        description="배정 시간대 등과 함께 새로운 일정을 등록합니다.",
        request=ScheduledTaskSerializer,
        responses={201: ScheduledTaskSerializer}
    )
  def post(self, request):
    start_time = request.data.get('start_time')
    end_time = request.data.get('end_time')
    is_locked = request.data.get('is_locked')
    task_id = request.data.get('task_id')
    task = Task.objects.get(id=task_id)
    if not start_time or not end_time or not is_locked:
      return Response({"detail": "[start_time, end_time, is_locked] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
    scheduled_task = Scheduled_task.objects.create(
                            start_time=start_time,
                            end_time=end_time,
                            is_locked=is_locked,
                            task_id=task)
    serializer = ScheduledTaskSerializer(scheduled_task)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class ScheduledTaskSingleView(APIView):
  @extend_schema(
        summary="배정된 일정 상세 조회",
        description="배정된 일정 1개의 상세 정보를 조회합니다.",
        responses={200: ScheduledTaskSerializer}
    )
  def get(self, request, scheduled_id):
    try:
      task = Scheduled_task.objects.get(id=scheduled_id)
    except:
      return Response({"single": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = ScheduledTaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  @extend_schema(
        summary="배정된 일정 삭제",
        description="배정된 일정을 삭제합니다.",
        responses={204: None}
    )
  def delete(self, request, scheduled_id):
    try:
      scheduled_task =  Scheduled_task.objects.get(id=scheduled_id)
    except:
      return Response({"single": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    scheduled_task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)