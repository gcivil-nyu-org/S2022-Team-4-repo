from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("homepage/", views.homepage_view, name="index"),
    path("set_location/<int:user_id>/", views.set_location, name="set_location"),
    path("pricing/", views.pricing_view, name="pricing"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.auth, name="auth"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("actvi/", views.actilink, name="activationlinkpage"),
    path("search/", views.search, name="search"),
    path("searchhard/", views.search_hardware, name="search_hardware"),
    path("profile/", views.profile_view, name="profile"),
    path("profile_editor/", views.profile_editor_view, name="profile_editor"),
    path("requestServices/", views.request_service_view, name="requestServices")
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]
