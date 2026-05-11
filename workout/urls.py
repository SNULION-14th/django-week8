from django.urls import path
from .views import WorkoutRecordListView, WorkoutRecordDetailView

urlpatterns = [
    path("", WorkoutRecordListView.as_view()),
    path("<int:record_id>/", WorkoutRecordDetailView.as_view()),
]