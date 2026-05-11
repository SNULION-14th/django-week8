from django.urls import path
# 추가
from .views import CalendarDetailView, CalendarListView, RoutineDetailView, RoutineListView, TodoDetailView, TodoListView

app_name = 'todo'

urlpatterns = [
    # --- TodoList ---
    path("todos/", TodoListView.as_view()), 
    path("<int:todo_id>/", TodoDetailView.as_view()), 

    # --- Calendar ---
    path("calendar/", CalendarListView.as_view()),
    path("<int:calendar_id>/", CalendarDetailView.as_view()),

    # --- Routine ---
    path("routine/", RoutineListView.as_view()),
    path("<int:routine_id>/", RoutineDetailView.as_view()),

]