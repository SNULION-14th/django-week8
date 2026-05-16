from django.urls import path
from ..views import SourceListView, SourceDetailView

app_name = 'notices'
urlpatterns = [
    path("", SourceListView.as_view()),
    path("<int:source_id>/", SourceDetailView.as_view()),
]
