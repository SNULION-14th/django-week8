from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

# Create your models here.
class User(AbstractUser):
  age = models.PositiveIntegerField(null=True)
  job = models.CharField(max_length=128, blank=True)
  gender = models.CharField(max_length=128, blank=True)
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.username}({self.id})'


class Interest(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="interests", on_delete=models.CASCADE)
  keyword = models.CharField(max_length=128)
  description = models.TextField()
  priority = models.IntegerField()
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.keyword}({self.id})'

