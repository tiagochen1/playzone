from django.urls import path

from .views import (
    CustomLoginView,
    register_view,
    password_reset_view,
    profile_view,
    logout_view,
)

app_name = "userauth"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    # Allow GET logout so users can click a simple link in the UI.
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("password-reset/", password_reset_view, name="password_reset"),
    path("profile/", profile_view, name="profile"),
]
