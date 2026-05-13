from rest_framework.serializers import ModelSerializer
from .models import UserProfile, Stock, Recommendation, Reason, Bookmark

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"

class RecommendationSerializer(ModelSerializer):
    class Meta:
        model = Recommendation
        fields = "__all__"

class ReasonSerializer(ModelSerializer):
    class Meta:
        model = Reason
        fields = "__all__"

class BookmarkSerializer(ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"