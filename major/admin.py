# ./major/admin.py

from django.contrib import admin
from .models import (
    User,
    Major,
    Lecture,
    CourseHistory,
    PreRequisiteRelation,
)

# admin 사이트에 모델 등록
admin.site.register(User)
admin.site.register(Major)
admin.site.register(Lecture)
admin.site.register(CourseHistory)
admin.site.register(PreRequisiteRelation)
