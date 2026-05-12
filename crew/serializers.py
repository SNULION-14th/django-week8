from rest_framework.serializers import ModelSerializer
from .models import Crew, CrewGoal

class CrewSerializer(ModelSerializer):
    class Meta:
        model = Crew
        fields = ["id", "name", "content", "created_at"]
        read_only_fields = ["id", "created_at"]

class CrewGoalSerializer(ModelSerializer):
    class Meta:
        model = CrewGoal
        fields = [
            "id",
            "crew",
            "title",
            "target_distance",
            "donation_amount",
            "start_date",
            "end_date",
            "is_achieved",
            "achieved_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "is_achieved",
            "achieved_at",
            "created_at",
        ]
