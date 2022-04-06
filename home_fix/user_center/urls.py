from django.urls import path
from . import views

app_name = "user_center"

urlpatterns = [
    path("index/", views.index_view, name="index"),
    path("request/", views.request_view, name="request"),
    path("provide/", views.provide_view, name="provide"),
    path("transaction/", views.transaction_view, name="transaction"),
    path("profile/", views.profile_view, name="profile"),
    path("profile_editor/", views.profile_editor_view, name="profile_editor"),
    path("request/", views.provide_view, name="request"),
    path(
        "request_finish_view/<int:order_id>",
        views.request_finish_view,
        name="request_finish",
    ),
    path("contact/", views.contact_view, name="contact"),
]
