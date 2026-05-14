from django.urls import path
from .views import TaskListView, TaskSingleView, TaskHistoryView, TaskHistorySingleView, ScheduledTaskView, ScheduledTaskSingleView

app_name = 'post'

# api/post/로 시작하는 url은 이곳으로 왔다.
# 그 이후에 붙는 것부터 여기서 찾는 것이다.
# 예) api/post/3이라면 <int:post_id>로
urlpatterns = [
    path("", TaskListView.as_view()),
    path("<int:task_id>/", TaskSingleView.as_view()),
    path("task_history/", TaskHistoryView.as_view()),
    path("task_history/<int:history_id>", TaskHistorySingleView.as_view()),
    path("scheduled_task/", ScheduledTaskView.as_view()),
    path("scheduled_task/<int:scheduled_id>", ScheduledTaskSingleView.as_view()),
]