from django.urls import path
from .views import SignupView, LoginView, LogoutView, ProfileDetailView

app_name = 'account'

urlpatterns = [
    # 회원가입
    path("signup/", SignupView.as_view(), name='signup'),
    
    # 로그인 / 로그아웃
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    
    # 내 정보 조회 (상세 보기)
    path("profile/", ProfileDetailView.as_view(), name='profile-detail'),
]