from django.contrib import admin
from .models import UserProfile, Stock, Recommendation, Reason, Bookmark   # 우리가 만든 Post 모델 불러오기

# admin 사이트에 Post 모델 등록
admin.site.register(UserProfile)
admin.site.register(Stock)
admin.site.register(Recommendation)
admin.site.register(Reason)
admin.site.register(Bookmark)