from django.conf import settings
from django.db import models


class Profile(models.Model):
    MODE_OFFLINE = 'OFFLINE'
    MODE_ONLINE = 'ONLINE'
    MODE_ANY = 'ANY'

    PREFERRED_MODE_CHOICES = [
        (MODE_OFFLINE, '대면'),
        (MODE_ONLINE, '비대면'),
        (MODE_ANY, '상관없음'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    department = models.CharField(max_length=100)
    student_year = models.IntegerField()
    is_double_major = models.BooleanField(default=False)
    is_returning_student = models.BooleanField(default=False)
    intro = models.TextField(blank=True)
    preferred_mode = models.CharField(
        max_length=20,
        choices=PREFERRED_MODE_CHOICES,
        default=MODE_ANY
    )

    def __str__(self):
        return f'{self.user.username} 프로필'


class Course(models.Model):
    course_code = models.CharField(max_length=50, unique=True)
    course_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.course_code} - {self.course_name}'


class CourseSection(models.Model):
    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'

    DAY_CHOICES = [
        (MONDAY, '월요일'),
        (TUESDAY, '화요일'),
        (WEDNESDAY, '수요일'),
        (THURSDAY, '목요일'),
        (FRIDAY, '금요일'),
        (SATURDAY, '토요일'),
        (SUNDAY, '일요일'),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    semester = models.CharField(max_length=20)
    professor = models.CharField(max_length=100)
    section_number = models.CharField(max_length=20)
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.course.course_name} {self.section_number}분반'


class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course_section = models.ForeignKey(
        CourseSection,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course_section'],
                name='unique_user_course_section'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.course_section}'


class Availability(models.Model):
    DAY_CHOICES = CourseSection.DAY_CHOICES

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.user.username} 공강 {self.day_of_week} {self.start_time}-{self.end_time}'


class ActivityType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    detail = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.detail:
            return f'{self.name} ({self.building}, {self.detail})'
        return f'{self.name} ({self.building})'


class MatchPost(models.Model):
    BASIS_COURSE = 'COURSE'
    BASIS_TIME = 'TIME'
    BASIS_COURSE_TIME = 'COURSE_TIME'

    MATCH_BASIS_CHOICES = [
        (BASIS_COURSE, '수업 기반'),
        (BASIS_TIME, '공강/시간 기반'),
        (BASIS_COURSE_TIME, '수업 + 시간 기반'),
    ]

    STATUS_OPEN = 'OPEN'
    STATUS_CLOSED = 'CLOSED'
    STATUS_CANCELED = 'CANCELED'

    STATUS_CHOICES = [
        (STATUS_OPEN, '모집중'),
        (STATUS_CLOSED, '마감'),
        (STATUS_CANCELED, '취소'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='match_posts'
    )
    course_section = models.ForeignKey(
        CourseSection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='match_posts'
    )
    activity_type = models.ForeignKey(
        ActivityType,
        on_delete=models.PROTECT,
        related_name='match_posts'
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='match_posts'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    match_basis = models.CharField(
        max_length=20,
        choices=MATCH_BASIS_CHOICES
    )
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    max_members = models.PositiveIntegerField(default=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MatchRequest(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CANCELED = 'CANCELED'

    STATUS_CHOICES = [
        (STATUS_PENDING, '대기'),
        (STATUS_ACCEPTED, '수락'),
        (STATUS_REJECTED, '거절'),
        (STATUS_CANCELED, '취소'),
    ]

    post = models.ForeignKey(
        MatchPost,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='match_requests'
    )
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'requester'],
                name='unique_post_requester'
            )
        ]

    def __str__(self):
        return f'{self.requester.username} → {self.post.title}'


class MatchGroup(models.Model):
    STATUS_ACTIVE = 'ACTIVE'
    STATUS_FINISHED = 'FINISHED'
    STATUS_CANCELED = 'CANCELED'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, '진행중'),
        (STATUS_FINISHED, '종료'),
        (STATUS_CANCELED, '취소'),
    ]

    post = models.OneToOneField(
        MatchPost,
        on_delete=models.CASCADE,
        related_name='group'
    )
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    ROLE_LEADER = 'LEADER'
    ROLE_MEMBER = 'MEMBER'

    ROLE_CHOICES = [
        (ROLE_LEADER, '리더'),
        (ROLE_MEMBER, '멤버'),
    ]

    group = models.ForeignKey(
        MatchGroup,
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'user'],
                name='unique_group_user'
            )
        ]

    def __str__(self):
        return f'{self.group.name} - {self.user.username}'


class MeetingSchedule(models.Model):
    group = models.ForeignKey(
        MatchGroup,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='meeting_schedules'
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f'{self.group.name} 일정'
