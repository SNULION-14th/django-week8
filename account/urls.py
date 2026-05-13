from django.urls import path
from .views import TeacherSignUpView, ParentSignUpView, StudentSignUpView, SignInView

app_name = 'account'
urlpatterns = [
    # CBV url path
    path("signup/teacher/", TeacherSignUpView.as_view()),
    path("signup/parent/", ParentSignUpView.as_view()),
    path("signup/student/", StudentSignUpView.as_view()),
    path("signin/", SignInView.as_view()),
]