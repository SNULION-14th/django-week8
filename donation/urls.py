# ./donation/urls.py

from django.urls import path
from .views import DonationListView, DonationDetailView

urlpatterns = [
    path("", DonationListView.as_view()),
    path("<int:donation_id>/", DonationDetailView.as_view()),
]