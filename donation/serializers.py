from rest_framework.serializers import ModelSerializer
from .models import Donation

class DonationSerializer(ModelSerializer):
  class Meta:
    model = Donation
    fields = [
            "id",
            "crew",
            "goal",
            "amount",
            "status",
            "created_at",
            "completed_at",
        ]
    read_only_fields = [
            "id",
            "crew",
            "goal",
            "amount",
            "created_at",
            "completed_at",
        ]