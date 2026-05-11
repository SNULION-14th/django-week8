from django.db import models

# Create your models here.
# ./account/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.IntegerField()
    major = models.CharField(max_length=255)

    def __str__(self):
        return f"id={self.id}, username={self.username}, age={self.age}, major={self.major}"