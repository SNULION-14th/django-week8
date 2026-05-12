
# Create your views here.
# ./post/views.py

from urllib import request

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import TodoList, Calendar, Routine
from .serializer import TodoListSerializer, RoutineSerializer, CalendarSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .request_serializers import TodoListRequestSerializer, CalendarRequestSerializer, RoutineRequestSerializer
from account.request_serializers import SignInRequestSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

## TodoList ##
class TodoListView(APIView):
    @extend_schema(
        summary="Todo 목록 조회",
        description="DB에 저장된 모든 Todo의 목록을 조회합니다.",
        responses={200: TodoListSerializer(many=True)}
    )
    
    def get(self, request): 
        todos = TodoList.objects.all() # TodoList를 다 가져와라
        serializer = TodoListSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="TodoList 생성 API",
        description="POST 요청 시 새로운 TodoList를 생성합니다. due_date는 YYYY-MM-DD 형식으로 보내주세요.",
        request=TodoListRequestSerializer,
        responses = {201: TodoListSerializer}
    )
    
    def post(self, request):
        serializer = TodoListRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_info = serializer.validated_data.get('user')
            username = user_info.get("username")
            password = user_info.get("password")
            
            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    return Response({"detail": "Password is incorrect."}, status=400)
                
                todo = TodoList.objects.create(
                    title=serializer.validated_data.get('title'),
                    due_date=serializer.validated_data.get('due_date'),
                    field=serializer.validated_data.get('field'),
                    priority=serializer.validated_data.get('priority'),
                    user=user
                )
                return Response(TodoListSerializer(todo).data, status=201)
            except User.DoesNotExist:
                return Response({"detail": "User Not found."}, status=404)
        return Response(serializer.errors, status=400)
            
            
class TodoDetailView(APIView):
    @extend_schema(
        summary="Todo 상세 조회",
        description="Todo 1개의 상세 정보를 조회합니다.",
        responses={200: TodoListSerializer}
    )
    def get(self, request,todo_id):
        try:
            todo = TodoList.objects.get(id=todo_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TodoListSerializer(instance=todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @extend_schema(
        summary="Todo 삭제",
        description="Todo를 삭제합니다.",
        request=SignInRequestSerializer,
        parameters=[
        OpenApiParameter(
            name="username",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="사용자 이름"
        ),
        OpenApiParameter(
            name="password",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="비밀번호"
        ),
    ],
        responses={204: None} # 204는 돌아오는 데이터가 없으므로 None
    )
    
    def delete(self, request, todo_id):
        try:
            todo = TodoList.objects.get(id=todo_id)
        except  TodoList.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        username = request.query_params.get("username")
        password = request.query_params.get("password")
        if not username or not password:
            return Response(
                {"detail": "[username, password] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if todo.user != user:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        ##delete가 계속 author field missing 에러가 나는데 잘 모르겠습니다ㅜㅜ##


    @extend_schema(
        summary="Todo 수정",
        description="게시글을 수정합니다.",
        request=TodoListRequestSerializer,
        responses={200: TodoListSerializer, 404: "Not Found", 400: "Bad Request"},
    )
    def put(self, request, todo_id):
        try:
            todo = TodoList.objects.get(id=todo_id)
        except:
            return Response(
                {"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )

        user_info = request.data.get('user')
        if not user_info:
            return Response(
                {"detail": "user field missing."}, status=status.HTTP_400_BAD_REQUEST
            )
        username = user_info.get("username")
        password = user_info.get("password")
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response(
                    {"detail": "Password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if todo.user != user:
                return Response(
                    {"detail": "You are not the author of this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        title = request.data.get("title")
        due_date = request.data.get("due_date")
        field = request.data.get("field")
        priority = request.data.get("priority")
        if not title or not due_date or not priority or not field:
            return Response(
                {"detail": "[title, due_date, priority, field] fields missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        todo.title = title
        todo.due_date = due_date
        todo.field = field
        todo.priority = priority

        todo.save()
        serializer = TodoListSerializer(instance=todo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
## Routine ##
class RoutineListView(APIView):
    @extend_schema(
        summary="Routine 목록 조회",
        responses={200: RoutineSerializer(many=True)}
    )
    def get(self, request): 
        routines = Routine.objects.all()
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Routine 생성",
        request=RoutineRequestSerializer,
        description="POST 요청 시 새로운 Routine을 생성합니다. time은 HH:MM:SS 형식으로 보내주세요.",
        responses={201: RoutineSerializer}
    )
    def post(self, request):
        serializer = RoutineRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_info = serializer.validated_data.get('user')
            username = user_info.get("username")
            password = user_info.get("password")
            
            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    return Response({"detail": "Password is incorrect."}, status=400)
                
                routine = Routine.objects.create(
                    title=serializer.validated_data.get('title'),
                    day=serializer.validated_data.get('day'),
                    time=serializer.validated_data.get('time'),
                    field=serializer.validated_data.get('field'),
                    user=user
                )
                return Response(RoutineSerializer(routine).data, status=201)
            except User.DoesNotExist:
                return Response({"detail": "User Not found."}, status=404)
        return Response(serializer.errors, status=400)

class RoutineDetailView(APIView):
    @extend_schema(summary="Routine 상세 조회", responses={200: RoutineSerializer})
    def get(self, request, routine_id):
        try:
            routine = Routine.objects.get(id=routine_id)
        except Routine.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        return Response(RoutineSerializer(routine).data, status=200)

    @extend_schema(summary="Routine 삭제", request=SignInRequestSerializer, 
                   parameters=[
        OpenApiParameter(
            name="username",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="사용자 이름"
        ),
        OpenApiParameter(
            name="password",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="비밀번호"
        ),
    ],responses={204: None})
    def delete(self, request, routine_id):
        try:
            routine = Routine.objects.get(id=routine_id)
        except Routine.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        username = request.query_params.get("username")
        password = request.query_params.get("password")
        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=400)
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"detail": "Password incorrect."}, status=400)
            if routine.user != user:
                return Response({"detail": "Forbidden."}, status=403)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        routine.delete()
        return Response(status=204)

    @extend_schema(summary="Routine 수정", request=RoutineRequestSerializer, responses={200: RoutineSerializer})
    def put(self, request, routine_id):
        try:
            routine = Routine.objects.get(id=routine_id)
        except Routine.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        user_info = request.data.get('user')
        username = user_info.get("username")
        try:
            user = User.objects.get(username=username)
            if not user.check_password(user_info.get("password")):
                return Response({"detail": "Password incorrect."}, status=400)
            if routine.user != user:
                return Response({"detail": "Forbidden."}, status=403)
        except:
            return Response({"detail": "User not found."}, status=404)

        # 필드 업데이트
        routine.title = request.data.get("title", routine.title)
        routine.day = request.data.get("day", routine.day)
        routine.time = request.data.get("time", routine.time)
        routine.field = request.data.get("field", routine.field)
        routine.save()
        
        return Response(RoutineSerializer(routine).data, status=200)
    
    ## Calendar ##
class CalendarListView(APIView):
    @extend_schema(summary="Calendar 목록 조회", responses={200: CalendarSerializer(many=True)})
    def get(self, request): 
        calendars = Calendar.objects.all()
        serializer = CalendarSerializer(calendars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="Calendar 생성", request=CalendarRequestSerializer, responses={201: CalendarSerializer})
    def post(self, request):
        serializer = CalendarRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_info = serializer.validated_data.get('user')
            try:
                user = User.objects.get(username=user_info.get("username"))
                if not user.check_password(user_info.get("password")):
                    return Response({"detail": "Password incorrect."}, status=400)
                
                calendar = Calendar.objects.create(
                    title=serializer.validated_data.get('title'),
                    date=serializer.validated_data.get('date'),
                    field=serializer.validated_data.get('field'),
                    user=user
                )
                return Response(CalendarSerializer(calendar).data, status=201)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=404)
        return Response(serializer.errors, status=400)

class CalendarDetailView(APIView):
    @extend_schema(summary="Calendar 상세 조회", responses={200: CalendarSerializer})
    def get(self, request, calendar_id):
        try:
            calendar = Calendar.objects.get(id=calendar_id)
        except Calendar.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)
        return Response(CalendarSerializer(calendar).data, status=200)

    @extend_schema(summary="Calendar 삭제", request=SignInRequestSerializer, 
                   parameters=[
        OpenApiParameter(
            name="username",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="사용자 이름"
        ),
        OpenApiParameter(
            name="password",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="비밀번호"
        ),], responses={204: None})
    def delete(self, request, calendar_id):
        try:
            calendar = Calendar.objects.get(id=calendar_id)
        except Calendar.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        username = request.query_params.get("username")
        password = request.query_params.get("password")
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"detail": "Password incorrect."}, status=400)
            if calendar.user != user:
                return Response({"detail": "Forbidden."}, status=403)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        calendar.delete()
        return Response(status=204)

    @extend_schema(summary="Calendar 수정", request=CalendarRequestSerializer, responses={200: CalendarSerializer})
    def put(self, request, calendar_id):
        try:
            calendar = Calendar.objects.get(id=calendar_id)
        except Calendar.DoesNotExist:
            return Response({"detail": "Not found."}, status=404)

        user_info = request.data.get('user')
        try:
            user = User.objects.get(username=user_info.get("username"))
            if not user.check_password(user_info.get("password")):
                return Response({"detail": "Password incorrect."}, status=400)
            if calendar.user != user:
                return Response({"detail": "Forbidden."}, status=403)
        except:
            return Response({"detail": "User not found."}, status=404)

        calendar.title = request.data.get("title", calendar.title)
        calendar.date = request.data.get("date", calendar.date)
        calendar.field = request.data.get("field", calendar.field)
        calendar.save()
        
        return Response(CalendarSerializer(calendar).data, status=200)