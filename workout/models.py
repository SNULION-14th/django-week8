from django.db import models
from django.conf import settings
from crew.models import Crew

class WorkoutRecord(models.Model):
    EXERCISE_TYPE_CHOICES = [
        ("running", "러닝"),
        ("walking", "걷기"),
        ("cycling", "자전거"),
        ("swimming", "수영"),
        ("hiking", "등산"),
        ("etc", "기타"),
    ]
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workout_records"
    )

    crew = models.ForeignKey(
        Crew,
        on_delete=models.CASCADE,
        related_name="workout_records"
    )

    exercise_type = models.CharField(
        max_length=20,
        choices=EXERCISE_TYPE_CHOICES
    )
    distance = models.FloatField()
    duration = models.PositiveIntegerField()
    record_date = models.DateField()
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.exercise_type} - {self.distance}km"