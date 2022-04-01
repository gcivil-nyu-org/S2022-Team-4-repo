import logging
from django.shortcuts import render, redirect
from users.models import CustomUser
from service.models import Services
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def request_service_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        services = Services.objects.all()
        user.password = None
        return render(
            request,
            "service/request_services.html",
            context={"user": user, "services": services},
        )
    else:
        return redirect("basic:index")


@csrf_exempt
def offer_service_view(request):
    if request.method == "POST":
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user.password = None
        logging.warning(request.POST["category"])
        Services.objects.create(
            service_category=request.POST["category"],
            user=request.user,
            service_description=request.POST["description"],
            coins_charged=request.POST["coins"],
            street=request.POST["address"],
            state=request.POST["state"],
            country=request.POST["country"],
            zip=request.POST["postalcode"],
            long=request.POST["long"],
            lat=request.POST["lat"],
        )
        return redirect("service:request_service")
    #        return render(request, "base/request_services.html", context={"user": user, "services": services})
    else:
        if request.user.is_authenticated:
            user_id = request.user.id
            user = CustomUser.objects.get(id=user_id)
            user.password = None
            return render(
                request, "service/offer_services.html", context={"user": user}
            )
        else:
            return redirect("basic:index")
