from atexit import register
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Create your views here.


def auth(request):
    return HttpResponseRedirect(reverse("authentication:index"))

def login_view(request):
    if request.user.is_authenticated:
        return redirect("authentication:index")
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            redirect("authentication:index")
        else:
            err = "Username or password is incorrect"
            return render(request, "authentication/login.html", {"error": err})

    return render(request, "authentication/login.html")


def set_location(request):
    return render(request, "authentication/search_location.html")


def homepage_view(request):
    return render(request, "authentication/homepage.html")


def logout_view(request):
    logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect("authentication:index")


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("authentication:login")
        else:
            # can show up message
            return render(
                request,
                "authentication/register.html",
                {'form': form}
            )
    else:
        form = CustomUserCreationForm()
        return render(
            request,
            "authentication/register.html",
            {'form': form}
        )
