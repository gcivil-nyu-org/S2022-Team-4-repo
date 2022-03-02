from atexit import register
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LocationForm
from django.contrib.auth import login, authenticate, logout


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


def set_location(request, user_id):
    context = {'user_id': user_id}
    if request.method == "POST":
        if request.user.id == user_id and request.user.is_authenticated:
            form = LocationForm(request.POST, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                print(user)
                user.save()
                return redirect("authentication:index")
            else:
                # add alert in future
                render(request, "authentication/set_location.html")
        #   illegal request. this user should not visit this page
        else:
            logout(request)
            redirect("authentication:index")
    else:
        re = request
        # if request.user.id == int(form.data.get("id")) and request.user.is_authenticated:
        return render(request, "authentication/set_location.html", context)


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
            return redirect("authentication:set_location", user_id=user.id)
        else:
            # can show up message
            return render(request, "authentication/register.html", {"form": form})
    else:
        form = CustomUserCreationForm()
        return render(request, "authentication/register.html", {"form": form})
