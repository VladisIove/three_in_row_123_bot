from django.urls import path
from user_core.views import MainPageWebApp

urlpatterns = [
    path("/", MainPageWebApp.as_view(template_name="about.html")),
]