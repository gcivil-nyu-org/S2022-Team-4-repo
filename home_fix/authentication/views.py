from atexit import register
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

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


def register_view(request):
    return render(request, "authentication/register.html")


def homepageview(request):
    return render(request, "authentication/homepage.html")


def logout_view(request):
    logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect("authentication:index")
