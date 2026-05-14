from django.urls import path
from .views import SignUpView, SignInView, FixedScheduleView, FixedScheduleSingleView

app_name = 'account'
urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("signin/", SignInView.as_view()),
    path("fixed_schedule/", FixedScheduleView.as_view()),
    path("fixed_schedule/<int:schedule_id>", FixedScheduleSingleView.as_view()),
]