from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ProfileViewSet,
    CourseViewSet,
    CourseSectionViewSet,
    EnrollmentViewSet,
    AvailabilityViewSet,
    ActivityTypeViewSet,
    PlaceViewSet,
    MatchPostViewSet,
    MatchRequestViewSet,
    MatchGroupViewSet,
    GroupMemberViewSet,
    MeetingScheduleViewSet,
)

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"course-sections", CourseSectionViewSet)
router.register(r"enrollments", EnrollmentViewSet)
router.register(r"availabilities", AvailabilityViewSet)
router.register(r"activity-types", ActivityTypeViewSet)
router.register(r"places", PlaceViewSet)
router.register(r"match-posts", MatchPostViewSet)
router.register(r"match-requests", MatchRequestViewSet)
router.register(r"match-groups", MatchGroupViewSet)
router.register(r"group-members", GroupMemberViewSet)
router.register(r"meeting-schedules", MeetingScheduleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]