# ./post/models.py

# Model 관련 fields, methods를 모아놓은 놈입니다
from django.db import models

# 현재 시간 알기 위해
from django.utils import timezone

from django.conf import settings

# models.Model을 상속하여 Post라는 class를 선언해줍니다
class Crew(models.Model):
    id = models.AutoField(primary_key=True)
	# title은 최대 256자의 character!
    name = models.CharField(max_length=256)
    
    # content는 글자 제한 없는 텍스트
    content = models.TextField()
    
    # created_at의 경우는 현재 시간 자동으로 입력되게!
    created_at = models.DateTimeField(default=timezone.now)

    # settings.AUTH_USER_MODEL로부터 유저 모델 참조
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)


	# 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.name
    
class CrewGoal(models.Model):
    id = models.AutoField(primary_key=True)
    crew = models.ForeignKey(
        Crew,
        on_delete = models.CASCADE,
        related_name="goals"
    )

    title = models.CharField(max_length=100)
    target_distance = models.FloatField()
    donation_amount = models.PositiveBigIntegerField()

    start_date = models.DateField()
    end_date = models.DateField()

    is_achieved = models.BooleanField(default=False)
    achieved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crew.name} - {self.title}"