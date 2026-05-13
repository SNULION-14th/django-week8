from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
  pw_hash = models.CharField(max_length=256)
  email = models.EmailField()
  name = models.CharField(max_length=128)
  age = models.PositiveIntegerField()
  job = models.CharField(max_length=128)
  gender = models.CharField(max_length=128)
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

