from django.urls import path
# 추가
from .views import CrewListView, CrewDetailView, CrewGoalListView, CrewGoalDetailView

app_name = 'crew'

# api/post/로 시작하는 url은 이곳으로 왔다.
# 그 이후에 붙는 것부터 여기서 찾는 것이다.
# 예) api/post/3이라면 <int:post_id>로
urlpatterns = [
    # CBV url path
    path("", CrewListView.as_view()), # 추가
    path("<int:crew_id>/", CrewDetailView.as_view()), # 추가
    path("goals/", CrewGoalListView.as_view()),
    path("goals/<int:goal_id>/", CrewGoalDetailView.as_view()),
]