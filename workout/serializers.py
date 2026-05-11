from rest_framework.serializers import ModelSerializer
from .models import WorkoutRecord

class WorkoutRecordSerializer(ModelSerializer):
    class Meta:
        model = WorkoutRecord
        fields = [
            "id",
            "user",
            "crew",
            "exercise_type",
            "distance",
            "duration",
            "record_date",
            "memo",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]