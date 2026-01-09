from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.urls import reverse_lazy

from .forms import RegisterForm

# Create your views here.

class CustomLoginView(LoginView):
    template_name = "userauth/login.html"
    redirect_authenticated_user = True


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("campos:list")
    else:
        form = RegisterForm()

    return render(request, "userauth/register.html", {"form": form})


def password_reset_view(request):
    return render(request, "userauth/password_reset.html")
