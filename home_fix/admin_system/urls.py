from django.urls import path
from . import views

app_name = "admin_system"
urlpatterns = [
    path("user", views.user_list_view, name="user"),
    path("report", views.report_list_view, name="report"),
]
