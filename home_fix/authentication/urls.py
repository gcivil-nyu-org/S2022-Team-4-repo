from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("", views.index_view, name="index")
]
