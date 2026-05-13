from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    trust_score = models.FloatField(default=36.5, help_text="매너 온도 (기본 36.5도)")

    def __str__(self):
        return self.username

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    university = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}의 프로필"