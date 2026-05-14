from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
  age = models.PositiveIntegerField(blank=True)
  job = models.CharField(max_length=128, blank=True)
  gender = models.CharField(max_length=128, blank=True)
  created_at = models.DateTimeField(default=timezone.now())

  def __str__(self):
    return f'{self.name}({self.id})'


class Interest(models.Model):
  user_id = models.ForeignKey("User", on_delete=models.CASCADE)
  keyword = models.CharField(default=128)
  description = models.TextField()
  priority = models.IntegerField()
  created_at = models.DateTimeField(default=timezone.now())

  def __str__(self):
    return f'{self.keyword}({self.id})'

