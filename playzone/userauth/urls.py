from django.urls import path

from .views import (
    CustomLoginView,
    register_view,
    profile_view,
    logout_view,
    UserPasswordResetView,
    UserPasswordResetDoneView,
    UserPasswordResetConfirmView,
    UserPasswordResetCompleteView,
)

app_name = "userauth"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    # Allow GET logout so users can click a simple link in the UI.
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("password-reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        UserPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password-reset/complete/", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("profile/", profile_view, name="profile"),
]
