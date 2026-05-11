from django.urls import path
# 추가
from .views import TodoDetailView, TodoListView

app_name = 'post'

urlpatterns = [
    # CBV url path
    path("", TodoListView.as_view()), # added
    path("<int:todo_id>/", TodoDetailView.as_view()), # added

]