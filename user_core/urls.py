from django.urls import path
from user_core.views import MainPageWebApp, GetOrCreateUser
from . import webhook


urlpatterns = [
    path("", MainPageWebApp.as_view()),
    path("get_or_create_user", GetOrCreateUser.as_view()),
    path('webhook/telegram/', webhook.telegram_webhook, name='telegram_webhook'),
]