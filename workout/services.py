from django.db.models import Sum
from django.utils import timezone

from crew.models import CrewGoal
from .models import WorkoutRecord
from donation.models import Donation


def check_crew_goal_achievement(crew):
    goals = CrewGoal.objects.filter(
        crew=crew,
        is_achieved=False
    )

    for goal in goals:
        total_distance = WorkoutRecord.objects.filter(
            crew=crew,
            record_date__gte=goal.start_date,
            record_date__lte=goal.end_date
        ).aggregate(total=Sum("distance"))["total"] or 0

        if total_distance >= goal.target_distance:
            goal.is_achieved = True
            goal.achieved_at = timezone.now()
            goal.save()

            Donation.objects.get_or_create(
                goal=goal,
                defaults={
                    "crew": crew,
                    "amount": goal.donation_amount,
                    "status": "pending",
                }
            )