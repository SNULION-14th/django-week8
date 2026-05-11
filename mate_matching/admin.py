from django.contrib import admin

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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'department',
        'student_year',
        'is_double_major',
        'is_returning_student',
        'preferred_mode',
    )
    search_fields = ('user__username', 'department')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_code', 'course_name', 'department')
    search_fields = ('course_code', 'course_name', 'department')


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'course',
        'semester',
        'professor',
        'section_number',
        'day_of_week',
        'start_time',
        'end_time',
    )
    search_fields = ('course__course_name', 'professor', 'semester')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course_section', 'created_at')
    search_fields = ('user__username', 'course_section__course__course_name')


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'day_of_week', 'start_time', 'end_time')
    search_fields = ('user__username',)


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'building', 'detail')
    search_fields = ('name', 'building')


@admin.register(MatchPost)
class MatchPostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'activity_type',
        'match_basis',
        'is_online',
        'max_members',
        'status',
        'created_at',
    )
    list_filter = ('match_basis', 'is_online', 'status', 'activity_type')
    search_fields = ('title', 'content', 'author__username')


@admin.register(MatchRequest)
class MatchRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'requester', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('post__title', 'requester__username')


@admin.register(MatchGroup)
class MatchGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'post__title')


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'user', 'role', 'joined_at')
    list_filter = ('role',)
    search_fields = ('group__name', 'user__username')


@admin.register(MeetingSchedule)
class MeetingScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group',
        'place',
        'start_at',
        'end_at',
        'is_online',
    )
    list_filter = ('is_online',)
    search_fields = ('group__name', 'place__name')