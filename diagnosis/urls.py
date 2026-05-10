from django.urls import path
from .views import DiagnosisListView

app_name = 'diagnosis'

urlpatterns = [
    path('report/', DiagnosisListView.as_view(), name='report-list'),
]