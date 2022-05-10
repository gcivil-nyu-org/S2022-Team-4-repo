from django.urls import path
from . import views

app_name = "admin_system"
urlpatterns = [
    # path("", views.admin_homepage, name="admin_index"),
    path("user", views.user_list_view, name="user"),
    path("report", views.report_list_view, name="report"),
    path(
        "user_froze_view/<int:user_id>",
        views.user_froze_view,
        name="user_froze",
    ),
    path(
        "user_unfroze_view/<int:user_id>",
        views.user_unfroze_view,
        name="user_unfroze",
    ),
]
