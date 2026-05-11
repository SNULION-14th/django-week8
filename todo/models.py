

# Model 관련 fields, methods를 모아놓은 놈입니다
from django.db import models

# 현재 시간 알기 위해
from django.utils import timezone

# models.Model을 상속하여 Post라는 class를 선언해줍니다
from django.db import models
from account.models import User
from seminar.settings import AUTH_USER_MODEL

DAY_CHOICES = [
    ('MON', '월요일'),
    ('TUE', '화요일'),
    ('WED', '수요일'),
    ('THU', '목요일'),
    ('FRI', '금요일'),
    ('SAT', '토요일'),
    ('SUN', '일요일'),
]

class Routine(models.Model):
    title = models.CharField(max_length=255)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    time = models.TimeField()
    field = models.CharField(max_length=255)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='routines')

class TodoList(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    field = models.CharField(max_length=255)
    priority = models.IntegerField()
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='todolists')

class Calendar(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(max_length=255)
    field = models.CharField(max_length=255)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendars')

	# 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title
    

