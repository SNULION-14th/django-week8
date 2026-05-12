from django.db import models
from crew.models import Crew

# Create your models here.
class Donation(models.Model):
    STATUS_CHOICES = [
      ("pending", "기부 예정"),
      ("completed", "기부 완료"),
    ]

    id = models.AutoField(primary_key=True)

    crew = models.ForeignKey(
      Crew,
      on_delete=models.CASCADE,
      related_name="donations"
    )

    goal = models.OneToOneField(
      "crew.CrewGoal",
      on_delete=models.CASCADE,
      related_name="donation"
    )

    amount = models.PositiveBigIntegerField()

    status = models.CharField(
      max_length =20,
      choices = STATUS_CHOICES,
      default = "pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
      return f"{self.crew.name} - {self.amount}원 기부"