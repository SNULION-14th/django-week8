from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  work_start_time = models.TimeField(blank=True)
  work_end_time = models.TimeField(blank=True)

  def __str__(self):
    return f"id={self.id}, username={self.username}"
  
class Fixed_schedule(models.Model):
  title = models.CharField(max_length=100)
  start_time = models.TimeField()
  end_time = models.TimeField()
  user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.schedule_id)