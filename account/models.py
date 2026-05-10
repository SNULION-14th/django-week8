# ./account/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    pre_diag = models.TextField(blank=True) # 기저 질환
    pre_med = models.TextField(blank=True)  # 복용 약물
    blood = models.CharField(max_length=5, blank=True)
    college = models.CharField(max_length=32, blank=True)
    major = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f"ID: {self.id} | Username: {self.username} | Major: {self.major}"