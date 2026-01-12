from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from .forms import RegisterForm

# Create your views here.

class CustomLoginView(LoginView):
    template_name = "userauth/login.html"
    redirect_authenticated_user = True


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("userauth:login")
    else:
        form = RegisterForm()

    return render(request, "userauth/register.html", {"form": form})


def password_reset_view(request):
    return render(request, "userauth/password_reset.html")

@login_required #impede os utilizadores que não tem conta acedam esta pagina
def profile_view(request):
    return render(request, "userauth/profile.html")
