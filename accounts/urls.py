from django.urls import path
from .views import SignUpView, SignInView, InterestListView, InterestDetailView
from notices.views import SourceSubscriptionListView, SourceSubscriptionDetailView, InboxNoticeListView, InboxNoticeDetailView

app_name = 'accounts'
urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("signin/", SignInView.as_view()),
    path("<int:user_id>/interests/", InterestListView.as_view()),
    path("<int:user_id>/interests/<int:interest_id>/", InterestDetailView.as_view()),
    path("<int:user_id>/subscriptions/", SourceSubscriptionListView.as_view()),
    path("<int:user_id>/subscriptions/<int:subscription_id>", SourceSubscriptionDetailView.as_view()),
    path("<int:user_id>/inbox/", InboxNoticeListView.as_view()),
    path("<int:user_id>/inbox/<int:inbox_id>/", InboxNoticeDetailView.as_view()),
]
