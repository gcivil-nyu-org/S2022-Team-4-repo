from django.urls import path
from . import views

app_name = "authentication"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("homepage/", views.homepage_view, name="index"),
    path("set_location/<int:user_id>/", views.set_location, name="set_location"),
    path("pricing/", views.pricing_view, name="pricing"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.auth, name="auth"),
]
