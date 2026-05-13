from django.db import models
from django.conf import settings

# Create your models here.
class Task(models.Model):
  # Enum definition (for "status" field)
  class Status(models.TextChoices):
    PENDING = 'PE', 'Pending'
    WORKING = 'WO', 'Working'
    DONE = 'DO', 'Done'

  title = models.CharField(max_length=100)
  category = models.CharField(max_length=20)
  priority = models.IntegerField()
  deadline = models.DateTimeField()
  estimated_duration = models.IntegerField()
  status = models.CharField(
    max_length=2,
    choices=Status.choices,
    default=Status.PENDING,
  )
  user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.title)
  

class Task_history(models.Model):
  planned_duration = models.IntegerField()
  actual_duration = models.IntegerField()
  completed_at = models.DateTimeField()
  user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
  task_id = models.OneToOneField(Task, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.history_id)
  
class Scheduled_task(models.Model):
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  is_locked = models.BooleanField()
  task_id = models.ForeignKey(Task, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.scheduled_id)