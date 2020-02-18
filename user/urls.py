from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("register/", views.register, name = "register"),
    path("login2/", views.login2, name = "login2"),
    path("logout2/", views.logout2, name = "logout"),
]