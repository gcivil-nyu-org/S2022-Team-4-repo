from django.urls import path
from . import views

app_name = "forum"
urlpatterns = [
    path("", views.forum, name="Forum"),
    path("discussion/<int:myid>/", views.discussion, name="Discussions"),
]
