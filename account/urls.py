# ./account/urls.py

from django.urls import path
from .views import SignUpView, SignInView

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
]
