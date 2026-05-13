from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ClassInfo, ClassLog
from .serializers import ClassInfoSerializer, ClassLogSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema(tags=["수업(ClassInfo) 관리"])
@extend_schema_view(
  list=extend_schema(summary="수업 목록 조회", description="로그인한 유저와 관련된 수업 목록을 가져옵니다."),
  retrieve=extend_schema(summary="수업 상세 조회", description="특정 수업의 상세 정보를 가져옵니다."),
  partial_update=extend_schema(summary="수업 정보 부분 수정", description="수업 정보 중 일부만 수정합니다.")
)
class ClassInfoViewSet(ModelViewSet):
  """
  수업 정보(ClassInfo) 관련 로직을 처리하는 ViewSet.
  로그인한 유저의 역할에 따라 본인과 관련된 수업 목록만 조회 가능.
  수업 생성, 수정, 삭제는 선생님만 가능.
  """

  queryset = ClassInfo.objects.all()
  serializer_class = ClassInfoSerializer
  permission_classes = [IsAuthenticated] # 로그인 상태 가정

  def get_queryset(self):
    # 로그인한 유저에 해당하는 수업만 필터링해서 가져오기
    user = self.request.user

    if user.role == 'teacher':
      return ClassInfo.objects.filter(teacher__user=user)
    elif user.role == 'parent':
      return ClassInfo.objects.filter(parent__user=user)
    elif user.role == 'student':
      return ClassInfo.objects.filter(student__user=user)

    return ClassInfo.objects.none()
  
  @extend_schema(
    summary="수업 생성",
    description="새로운 과외 수업을 생성합니다. 선생님 유저만 생성 가능합니다.",
    request=ClassInfoSerializer,
    responses={201: ClassInfoSerializer, 403: "Forbidden"},
  ) 
  def create(self, request, *args, **kwargs):
    # 선생님만 수업 생성 가능
    if request.user.role != 'teacher':
      return Response({"detail": "선생님만 수업을 생성할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

    return super().create(request, *args, **kwargs)

  def perform_create(self, serializer):
    # 수업 생성시 로그인된 선생님 정보를 자동 할당
    serializer.save(teacher=self.request.user.teacher)

  @extend_schema(
    summary="수업 정보 수정",
    description="수업 정보를 수정합니다. 해당 수업을 담당하는 선생님만 수정 가능합니다.",
    request=ClassInfoSerializer,
    responses={200: ClassInfoSerializer, 403: "Forbidden", 404: "Not Found"},
  )
  def update(self, request, *args, **kwargs):
    if request.user.role != 'teacher':
      return Response({"detail": "선생님만 수업 정보를 수정할 수 있습니다"}, status=status.HTTP_403_FORBIDDEN)

    instance = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
    return super().update(request, *args, **kwargs)

  @extend_schema(
    summary="수업 정보 삭제",
    description="수업 정보를 삭제합니다. 해당 수업을 담당하는 선생님만 삭제 가능합니다.",
    responses={204: "No Content", 403: "Forbidden", 404: "Not Found"},
  )
  def destroy(self, request, *args, **kwargs):
    if request.user.role != 'teacher':
      return Response({"detail": "선생님만 수업 정보를 삭제할 수 있습니다"}, status=status.HTTP_403_FORBIDDEN)

    instance = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
    return super().destroy(request, *args, **kwargs)

@extend_schema(tags=["수업 일지(ClassLog) 관리"])
@extend_schema_view(
  list=extend_schema(summary="수업 일지 목록 조회", description="해당 수업의 수업 일지 목록을 가져옵니다."),
  retrieve=extend_schema(summary="수업 일지 상세 조회", description="특정 수업 일지의 상세 정보를 가져옵니다."),
  partial_update=extend_schema(summary="수업 일지 부분 수정", description="수업 일지 중 일부만 수정합니다.")
)
class ClassLogViewSet(ModelViewSet): 
  """
  수업 일지(ClassLog) 관련 로직을 처리하는 ViewSet.
  일지 작성, 수정, 삭제는 수업 담당 선생님만 가능.
  """

  serializer_class = ClassLogSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    class_info_id = self.kwargs.get('class_info_id')
    
    # 유저 관련 수업 정보 목록 가져오기
    if user.role == 'teacher':
      classes = ClassInfo.objects.filter(teacher__user=user)
    elif user.role == 'parent':
      classes = ClassInfo.objects.filter(parent__user=user)
    elif user.role == 'student':
      classes = ClassInfo.objects.filter(student__user=user)

    # 요청받은 class_info_id와 일치하는 수업 찾기
    class_info = classes.filter(id=class_info_id).first()

    # 권한이 없는 수업인 경우 None을 반환
    if not class_info:
      return ClassLog.objects.none()

    return ClassLog.objects.filter(class_info=class_info)

  @extend_schema(
    summary="수업 일지 생성",
    description="수업 일지를 작성합니다. 해당 수업을 담당하는 선생님만 작성 가능합니다.",
    request=ClassLogSerializer,
    responses={201: ClassLogSerializer, 403: "Forbidden", 404: "Not Found"},
  )
  def create(self, request, *args, **kwargs):
    class_info_id = self.kwargs.get('class_info_id')
    class_info = get_object_or_404(ClassInfo, id=class_info_id)

    if class_info.teacher.user != request.user:
      return Response({"detail": "본인의 수업 일지만 작성할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

    return super().create(request, *args, **kwargs)

  def perform_create(self, serializer):
    class_info_id = self.kwargs.get('class_info_id')
    serializer.save(class_info_id=class_info_id)

  @extend_schema(
    summary="수업 일지 수정",
    description="수업 일지를 수정합니다. 해당 일지를 작성한 선생님만 수정 가능합니다.",
    request=ClassLogSerializer,
    responses={200: ClassLogSerializer, 403: "Forbidden", 404: "Not Found"},
  )
  def update(self, request, *args, **kwargs):
    if request.user.role != 'teacher':
      return Response({"detail": "선생님만 수업 일지를 수정할 수 있습니다"}, status=status.HTTP_403_FORBIDDEN)

    instance = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
    return super().update(request, *args, **kwargs)

  @extend_schema(
    summary="수업 일지 삭제",
    description="수업 일지를 삭제합니다. 해당 일지를 작성한 선생님만 삭제 가능합니다.",
    responses={204: "No Content", 403: "Forbidden", 404: "Not Found"},
  )
  def destroy(self, request, *args, **kwargs):
    if request.user.role != 'teacher':
      return Response({"detail": "선생님만 수업 일지를 삭제할 수 있습니다"}, status=status.HTTP_403_FORBIDDEN)

    instance = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
    return super().destroy(request, *args, **kwargs)