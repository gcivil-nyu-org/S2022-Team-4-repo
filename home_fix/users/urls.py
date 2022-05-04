from django.urls import path
from . import views
from .views import CreateCheckoutSessionView

app_name = "users"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("set_location/<int:user_id>/", views.set_location, name="set_location"),
    path("pricing/", views.pricing_view, name="pricing"),
    path(
        "create-checkout-session/<pk>",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("webhooks/stripe", views.stripe_webhook, name="stripe-webhook"),
    path("logout/", views.logout_view, name="logout"),
    # path("", views.auth, name="auth"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("actvi/", views.actilink, name="activationlinkpage"),
    path("about/", views.about_page, name="about"),
    path("privacy/", views.privacy_page, name="privacy"),
]
