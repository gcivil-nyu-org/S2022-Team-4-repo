from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from service.models import Services, Order

# Create your views here.
def search(request):
    if not request.user.is_authenticated:
        return redirect("users:login")
    User = get_user_model()
    users = User.objects.all()
    userloc = [float(request.user.lat), float(request.user.long)]
    locations = []
    for i in users:
        temp = []
        if i.lat is None or i.long is None:
            print(i)
            continue
        temp.append(float(i.lat))
        temp.append(float(i.long))
        locations.append(temp)

    return render(
        request,
        "map/locs.html",
        context={
            "base": locations,
            "user": userloc,
        },
    )


def search_hardware(request):
    if not request.user.is_authenticated:
        return redirect("users:login")
    User = get_user_model()
    users = User.objects.all()
    locations = []
    for i in users:
        temp = []
        if i.lat is None or i.long is None:
            print(i)
            continue
        temp.append(float(i.lat))
        temp.append(float(i.long))
        temp.append(i.first_name)
        temp.append(i.email)
        temp.append(i.street)
        locations.append(temp)
    userloc = [float(request.user.lat), float(request.user.long)]

    return render(
        request,
        "map/locs_hardware.html",
        context={"base": locations, "user_loc": userloc, "users": users},
    )
