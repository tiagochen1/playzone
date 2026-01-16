from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, register_view, password_reset_view, profile_view

app_name = "userauth"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="campos:campos_list"), name="logout"),
    path("register/", register_view, name="register"),
    path("password-reset/", password_reset_view, name="password_reset"),
    path("profile/", profile_view, name="profile"),
]
