from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import (
    Profile,
    Course,
    CourseSection,
    Enrollment,
    Availability,
    ActivityType,
    Place,
    MatchPost,
    MatchRequest,
    MatchGroup,
    GroupMember,
    MeetingSchedule,
)

from .serializers import (
    ProfileSerializer,
    CourseSerializer,
    CourseSectionSerializer,
    EnrollmentSerializer,
    AvailabilitySerializer,
    ActivityTypeSerializer,
    PlaceSerializer,
    MatchPostSerializer,
    MatchRequestSerializer,
    MatchGroupSerializer,
    GroupMemberSerializer,
    MeetingScheduleSerializer,
)


def crud_schema(tag, label, description):
    """
    ViewSet의 CRUD API에 한글 Swagger 설명을 일괄 적용하는 데코레이터
    """

    return extend_schema_view(
        list=extend_schema(
            summary=f"{label} 목록 조회",
            description=f"{description} 목록을 조회합니다.",
            tags=[tag],
        ),
        create=extend_schema(
            summary=f"{label} 생성",
            description=f"새로운 {description} 데이터를 생성합니다.",
            tags=[tag],
        ),
        retrieve=extend_schema(
            summary=f"{label} 상세 조회",
            description=f"특정 {description} 데이터의 상세 정보를 조회합니다.",
            tags=[tag],
        ),
        update=extend_schema(
            summary=f"{label} 전체 수정",
            description=f"특정 {description} 데이터의 전체 정보를 수정합니다.",
            tags=[tag],
        ),
        partial_update=extend_schema(
            summary=f"{label} 일부 수정",
            description=f"특정 {description} 데이터의 일부 필드만 수정합니다.",
            tags=[tag],
        ),
        destroy=extend_schema(
            summary=f"{label} 삭제",
            description=f"특정 {description} 데이터를 삭제합니다.",
            tags=[tag],
        ),
    )


@crud_schema("profiles", "프로필", "사용자 프로필")
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer


@crud_schema("courses", "과목", "과목")
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


@crud_schema("course-sections", "강의 분반", "특정 학기의 강의 분반")
class CourseSectionViewSet(viewsets.ModelViewSet):
    queryset = CourseSection.objects.select_related("course").all()
    serializer_class = CourseSectionSerializer


@crud_schema("enrollments", "수강 등록", "사용자의 수강 과목 등록 정보")
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related(
        "user",
        "course_section",
        "course_section__course",
    ).all()
    serializer_class = EnrollmentSerializer


@crud_schema("availabilities", "공강 시간", "사용자의 공강 시간")
class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.select_related("user").all()
    serializer_class = AvailabilitySerializer


@crud_schema("activity-types", "활동 유형", "밥약, 카공, 스터디, 문풀, 오픈채팅 등의 활동 유형")
class ActivityTypeViewSet(viewsets.ModelViewSet):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer


@crud_schema("places", "장소", "캠퍼스 내 모임 장소")
class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


@crud_schema("match-posts", "모집글", "수업·공강 기반 매칭 모집글")
class MatchPostViewSet(viewsets.ModelViewSet):
    queryset = MatchPost.objects.select_related(
        "author",
        "course_section",
        "course_section__course",
        "activity_type",
        "place",
    ).all()
    serializer_class = MatchPostSerializer


@crud_schema("match-requests", "참여 신청", "모집글에 대한 참여 신청")
class MatchRequestViewSet(viewsets.ModelViewSet):
    queryset = MatchRequest.objects.select_related(
        "post",
        "post__author",
        "requester",
    ).all()
    serializer_class = MatchRequestSerializer


@crud_schema("match-groups", "매칭 그룹", "성사된 스터디·밥약·카공 매칭 그룹")
class MatchGroupViewSet(viewsets.ModelViewSet):
    queryset = MatchGroup.objects.select_related(
        "post",
        "post__author",
        "post__activity_type",
    ).all()
    serializer_class = MatchGroupSerializer


@crud_schema("group-members", "그룹 멤버", "매칭 그룹에 참여한 사용자")
class GroupMemberViewSet(viewsets.ModelViewSet):
    queryset = GroupMember.objects.select_related(
        "group",
        "group__post",
        "user",
    ).all()
    serializer_class = GroupMemberSerializer


@crud_schema("meeting-schedules", "모임 일정", "매칭 그룹의 실제 모임 일정")
class MeetingScheduleViewSet(viewsets.ModelViewSet):
    queryset = MeetingSchedule.objects.select_related(
        "group",
        "group__post",
        "place",
    ).all()
    serializer_class = MeetingScheduleSerializer