import logging
from django.shortcuts import render, redirect
from users.models import CustomUser
from service.models import Services, Order
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def request_service_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        services = Services.objects.filter(visible=True)
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
        # can add some params validation
        print(request.POST)
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


def request_service_confirm_view(request, service_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        service = Services.objects.get(id=service_id)
        Order.objects.create(user=user, service=service)
        service.visible = False
        service.save()
        return redirect("user_center:request")
    else:
        return redirect("basic:index")


def service_detail_view(request, service_id):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        services = list(Services.objects.filter(id=service_id).all())
        logging.warning(services)
        user.password = None
        return render(
            request,
            "service/service_detail.html",
            context={"user": user, "services": services[0]},
        )
    else:
        return redirect("basic:index")
