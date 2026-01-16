from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .forms import RegisterForm

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy

# Create your views here.

class CustomLoginView(LoginView):
    template_name = "userauth/login.html"
    redirect_authenticated_user = True


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("UTILIZADOR CRIADO:", user.username)
            return redirect("userauth:login")
        else:
            print("ERROS DO FORM:", form.errors)  # 👈 OBRIGATÓRIO
    else:
        form = RegisterForm()

    return render(request, "userauth/register.html", {"form": form})

class UserPasswordResetView(PasswordResetView):
    template_name = "userauth/password_reset.html"
    email_template_name = "userauth/emails/password_reset_email.txt"
    subject_template_name = "userauth/emails/password_reset_subject.txt"
    success_url = reverse_lazy("userauth:password_reset_done")


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "userauth/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "userauth/password_reset_confirm.html"
    success_url = reverse_lazy("userauth:password_reset_complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "userauth/password_reset_complete.html"


def password_reset_view(request):
    return render(request, "userauth/password_reset.html")

@login_required #impede os utilizadores que não tem conta acedam esta pagina
def profile_view(request):
    return render(request, "userauth/profile.html")
