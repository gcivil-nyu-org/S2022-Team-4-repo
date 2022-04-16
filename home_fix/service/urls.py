from django.urls import path
from . import views

app_name = "service"
urlpatterns = [
    path("request_service/", views.request_service_view, name="request_service"),
    path("offer_service/", views.offer_service_view, name="offer_service"),
    path("services_locations/", views.services_locations, name="services_locations"),
    path(
        "request_service_confirm/<int:service_id>",
        views.request_service_confirm_view,
        name="request_service_confirm",
    ),
    path(
        "service_detail/<int:service_id>",
        views.service_detail_view,
        name="service_detail",
    ),
    path("report/<int:service_id>", views.report_view, name="report"),
]
