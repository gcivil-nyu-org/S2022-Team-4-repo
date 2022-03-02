from atexit import register
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Create your views here.


def auth(request):
    return render(request, "authentication/auth.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("authentication:index")
    if request.method == "POST":
        # redirect(request,'authentication/register.html')
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            redirect("authentication:index")
            # print(request.get_full_path())
            # print("url: ", request.GET.get("next"))
            # next_url = request.GET.get("next")
            # if next_url:
            #     return redirect(next_url)
            # else:
            #     return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.info(request, "Username OR password is incorrect")

    context = {}
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
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        return render(
            request,
            "authentication/register.html",
        )
