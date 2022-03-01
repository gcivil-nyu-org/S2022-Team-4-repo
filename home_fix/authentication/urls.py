from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("homepage/", views.homepage_view, name="index"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.auth, name="auth"),
]
