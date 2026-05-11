from rest_framework import serializers

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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = "__all__"


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = "__all__"


class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = "__all__"


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"


class MatchPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchPost
        fields = "__all__"


class MatchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRequest
        fields = "__all__"


class MatchGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchGroup
        fields = "__all__"


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = "__all__"


class MeetingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingSchedule
        fields = "__all__"