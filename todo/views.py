
# Create your views here.
# ./post/views.py

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import TodoList, Calendar, Routine
from .serializer import TodoListSerializer, RoutineSerializer, CalendarSerializer
from drf_spectacular.utils import extend_schema

## TodoList ##
class TodoListView(APIView):
    @extend_schema(
        summary="Todo 목록 조회",
        description="DB에 저장된 모든 Todo의 목록을 조회합니다.",
        responses={200: TodoListSerializer(many=True)}
    )
    
    def get(self): 
        todos = TodoList.objects.all() # TodoList를 다 가져와라
        serializer = TodoListSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="TodoList 생성 API",
        description="POST 요청 시 새로운 TodoList를 생성합니다. due_date는 YYYY-MM-DD 형식으로 보내주세요.",
        request=TodoListSerializer,
        responses = {201: TodoListSerializer}
    )
    
    def post(self, request):
        title = request.data.get('title')
        due_date = request.data.get('due_date')
        field = request.data.get('field')
        priority = request.data.get('priority')
        user = request.user
        if not title or not due_date:
            return Response({"detail": "[title, due_date] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        todo = TodoList.objects.create(title=title, due_date=due_date, field=field, priority=priority, user=user)
        serializer = TodoListSerializer(todo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            
class TodoDetailView(APIView):
    @extend_schema(
        summary="Todo 상세 조회",
        description="Todo 1개의 상세 정보를 조회합니다.",
        responses={200: TodoListSerializer}
    )
    def get(self, todo_id):
        try:
            todo = TodoList.objects.get(id=todo_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoListSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @extend_schema(
        summary="Todo 삭제",
        description="Todo를 삭제합니다.",
        responses={204: None} # 204는 돌아오는 데이터가 없으므로 None
    )
    
    def delete(self, todo_id):
        try:
            todo = TodoList.objects.get(id=todo_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
## Routine ##
class RoutineListView(APIView):
    @extend_schema(
        summary="Routine 목록 조회",
        description="모든 루틴의 목록을 조회합니다.",
        responses={200: RoutineSerializer(many=True)}
    )
    def get(self): 
        routines = Routine.objects.all()
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Routine 생성",
        description="새로운 루틴을 생성합니다. day는 ['MON', 'TUE'...] 형식으로 보내주세요.",
        request=RoutineSerializer,
        responses={201: RoutineSerializer}
    )
    def post(self, request):
        title = request.data.get('title')
        day = request.data.get('day')
        time = request.data.get('time')
        field = request.data.get('field')
        user = request.user
        
        if not title or not day or not time:
            return Response({"detail": "[title, day, time] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        # user는 현재 로그인한 유저를 자동으로 할당 (또는 request에서 받기)
        routine = Routine.objects.create(
            title=title, day=day, time=time, field=field, user=user
        )
        serializer = RoutineSerializer(routine)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RoutineDetailView(APIView):
    @extend_schema(summary="Routine 상세 조회", responses={200: RoutineSerializer})
    def get(self, request, routine_id):
        try:
            routine = Routine.objects.get(id=routine_id)
        except Routine.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RoutineSerializer(routine)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="Routine 삭제", responses={204: None})
    def delete(self, request, routine_id):
        try:
            routine = Routine.objects.get(id=routine_id)
        except Routine.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    ## Calendar ##
class CalendarListView(APIView):
    @extend_schema(
        summary="Calendar 일정 목록 조회",
        responses={200: CalendarSerializer(many=True)}
    )
    def get(self): 
        calendars = Calendar.objects.all()
        serializer = CalendarSerializer(calendars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Calendar 일정 생성",
        request=CalendarSerializer,
        responses={201: CalendarSerializer}
    )
    def post(self, request):
        title = request.data.get('title')
        date = request.data.get('date')
        field = request.data.get('field')
        user = request.user
        if not title or not date:
            return Response({"detail": "[title, date] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        calendar = Calendar.objects.create(
            title=title, date=date, field=field, user=user
        )
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CalendarDetailView(APIView):
    @extend_schema(summary="Calendar 상세 조회", responses={200: CalendarSerializer})
    def get(self, calendar_id):
        try:
            calendar = Calendar.objects.get(id=calendar_id)
        except Calendar.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="Calendar 삭제", responses={204: None})
    def delete(self, calendar_id):
        try:
            calendar = Calendar.objects.get(id=calendar_id)
        except Calendar.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)