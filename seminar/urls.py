# ./seminar/urls.py

from django.contrib import admin
from django.urls import path, include
# 추가
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chat/', include('chat.urls')),

    # 추가
    # 명세 파일 다운로드
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger 문서 진입
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
