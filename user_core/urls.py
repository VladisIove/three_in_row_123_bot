from django.urls import path
from user_core.views import MainPageWebApp, GetOrCreateUser

urlpatterns = [
    path("", MainPageWebApp.as_view()),
    path("/get_or_create_user", GetOrCreateUser.as_view()),
]