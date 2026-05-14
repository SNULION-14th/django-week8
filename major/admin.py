from django.contrib import admin
from .models import (
    Student,
    Department,
    Course,
    Interest,
    StudentInterest,
    DepartmentInterest,
    Recommendation,
)

admin.site.register(Student)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Interest)
admin.site.register(StudentInterest)
admin.site.register(DepartmentInterest)
admin.site.register(Recommendation)