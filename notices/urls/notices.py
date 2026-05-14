from django.urls import path
from ..views import NoticeListView, NoticeDetailView

app_name = 'notices'
urlpatterns = [
    path("", NoticeListView.as_view()),
    path("<int:notice_id>/", NoticeDetailView.as_view()),
]
