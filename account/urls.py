from django.urls import path
from .views import ProfileListView, ProfileDetailView

app_name = 'account'

urlpatterns = [
    path('profile/', ProfileListView.as_view(), name='profile-list'),
    path('profile/<int:profile_id>/', ProfileDetailView.as_view(), name='profile-detail'),
]