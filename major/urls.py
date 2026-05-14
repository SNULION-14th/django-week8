from django.urls import path

from .views import (
    StudentListView,
    StudentDetailView,
    DepartmentListView,
    DepartmentDetailView,
    CourseListView,
    CourseDetailView,
    InterestListView,
    InterestDetailView,
    StudentInterestListView,
    StudentInterestDetailView,
    DepartmentInterestListView,
    DepartmentInterestDetailView,
    RecommendationListView,
    RecommendationDetailView,
)

urlpatterns = [
    path('students/', StudentListView.as_view()),
    path('students/<int:student_id>/', StudentDetailView.as_view()),

    path('departments/', DepartmentListView.as_view()),
    path('departments/<int:department_id>/', DepartmentDetailView.as_view()),

    path('courses/', CourseListView.as_view()),
    path('courses/<int:course_id>/', CourseDetailView.as_view()),

    path('interests/', InterestListView.as_view()),
    path('interests/<int:interest_id>/', InterestDetailView.as_view()),

    path('student-interests/', StudentInterestListView.as_view()),
    path('student-interests/<int:student_interest_id>/', StudentInterestDetailView.as_view()),

    path('department-interests/', DepartmentInterestListView.as_view()),
    path('department-interests/<int:department_interest_id>/', DepartmentInterestDetailView.as_view()),

    path('recommendations/', RecommendationListView.as_view()),
    path('recommendations/<int:recommendation_id>/', RecommendationDetailView.as_view()),
]