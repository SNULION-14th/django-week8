"""
URL configuration for seminar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/crew/', include('crew.urls')), # post/의 urls.py 파일로 가서 url을 찾아라
    path("api/workout/", include("workout.urls")),
    path("api/donation/", include("donation.urls")),
    path("api/account/", include("account.urls")),
    # 명세 파일 다운로드
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger 문서 진입
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
