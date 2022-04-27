from django.shortcuts import render, redirect

from admin_system.models import Report
from service.models import Services
from users.models import CustomUser, Product


#
# def admin_homepage(request):
#     return render(request, "admin_system/index.html")


def report_list_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "GET":
            list1 = Report.objects.all().order_by("-timestamp")
            return render(
                request, "admin_system/report.html", context={"reports": list1}
            )
        else:
            report_id = request.POST.get("report_id")
            report_action = request.POST.get("report_action")
            list1 = Report.objects.all().order_by("-timestamp")
            try:
                report = Report.objects.get(id=report_id)
            except Report.DoesNotExist:
                return render(
                    request, "admin_system/report.html", context={"reports": list1}
                )
            if report_action == "0":
                service = report.service
                service.visible = False
                service.save()
                report.status = "deleted"
                report.save()
            if report_action == "1":
                report.status = "withdraw"
                report.save()
            return render(
                request, "admin_system/report.html", context={"reports": list1}
            )
    else:
        return redirect("users:login")


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
        return redirect("users:login")
