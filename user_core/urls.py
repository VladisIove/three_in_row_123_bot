from django.urls import path
from user_core.views import GetOrCreateUser, AIChat, FeedbackView
from . import webhook


urlpatterns = [
    path("get_or_create_user", GetOrCreateUser.as_view()),
    path("api/chat", AIChat.as_view()),
    path("api/feedback", FeedbackView.as_view()),
    path('webhook/telegram/', webhook.telegram_webhook, name='telegram_webhook'),
]