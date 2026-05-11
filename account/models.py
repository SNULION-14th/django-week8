from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
   GENDER_CHOICES = [
        ("male", "남성"),
        ("female", "여성"),
        ("other", "기타"),
    ]
   gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )
   age = models.PositiveIntegerField(
        null=True,
        blank=True
    )
   
   def __str__(self):
        return f"id={self.id}, username={self.username}, gender={self.gender}, age={self.age}"