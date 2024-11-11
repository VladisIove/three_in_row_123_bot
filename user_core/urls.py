from django.urls import path
from views import MainPageWebApp

urlpatterns = [
    path("/", MainPageWebApp.as_view(template_name="about.html")),
]