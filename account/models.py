from django.db import models

# Create your models here.
# ./account/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    major = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"id={self.id}, username={self.username}, email={self.email}, age={self.age}, major={self.major}"