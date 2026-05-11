# post/models.py

# Model 관련 fields, methods를 모아놓은 놈입니다
from django.db import models
# 현재 시간 알기 위해
from django.utils import timezone
# 지금 우리가 관심 있는건 settings에서 선언한 유저 모델
from django.conf import settings
# rating 범위 검증
from django.core.validators import MinValueValidator, MaxValueValidator

from tag.models import Tag

# models.Model을 상속하여 Post라는 class를 선언해줍니다
class Post(models.Model):
		# title은 최대 256자의 character!
    title = models.CharField(max_length=256)
    
    # content는 글자 제한 없는 텍스트
    content = models.TextField()
    
    # created_at의 경우는 현재 시간 자동으로 입력되게!
    created_at = models.DateTimeField(default=timezone.now)

    # settings.AUTH_USER_MODEL로부터 유저 모델 참조
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    # 좋아요 누른 유저들
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_posts', through='Like')
    
    # 포스트에 달린 태그들
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # 이건 print하면 어떤 값을 return할 지 알려주는 것!
    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class Exhibition(models.Model):
    exhibition_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class Log(models.Model):
    log_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='logs',
    )

    exhibition = models.ForeignKey(
        Exhibition,
        on_delete=models.CASCADE,
        related_name='logs',
    )

    content = models.TextField()

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.exhibition.title}"


class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)

    log = models.ForeignKey(
        Log,
        on_delete=models.CASCADE,
        related_name='photos',
    )

    image_url = models.URLField(max_length=500)

    def __str__(self):
        return f"Photo {self.photo_id} of Log {self.log_id}"