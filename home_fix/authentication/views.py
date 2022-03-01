from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.



def auth(request):
    return render(request, "authentication/auth.html")


def login_view(request):
    return render(request, "authentication/login.html")


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("authentication:auth")
        else:
            # can show up message
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request, "authentication/register.html")
    else:
        return render(request, "authentication/register.html", )
