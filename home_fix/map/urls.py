from django.urls import path
from . import views

app_name = "map"
urlpatterns = [
    path("search/", views.search, name="search"),
    path("searchhard/", views.search_hardware, name="search_hardware"),
]
