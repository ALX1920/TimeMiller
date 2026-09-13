from django.urls import path

from . import views

app_name = "visits"

urlpatterns = [
    path("", views.get_visits, name="get_visits"),
    path("register/", views.register_visit, name="register_visit"),
]
