from django.shortcuts import render, redirect

from admin_system.models import Report
from service.models import Services
from users.models import CustomUser, Product


def report_list_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "GET":
            list1 = Report.objects.all().order_by("-timestamp")
            return render(
                request, "admin_system/report.html", context={"reports": list1}
            )
        else:
            report_id = request.POST.get("report_id")
            report = Report.objects.get(id=report_id)
            report.status = "solved"
            report.save()
            list1 = Report.objects.all().order_by("-timestamp")
            return render(
                request, "admin_system/report.html", context={"reports": list1}
            )
    else:
        return redirect("basic:index")


def user_list_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        users = CustomUser.objects.all().order_by("is_staff")
        product = Product.objects.all().order_by("id")
        return render(
            request,
            "admin_system/user.html",
            context={"users": users, "product": product},
        )
    else:
        return redirect("basic:index")
