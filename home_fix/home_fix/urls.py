"""home_fix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.base, name='base')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='base')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from cgitb import handler
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("basic.urls")),
    path("users/", include("users.urls")),
    path("map/", include("map.urls")),
    path("service/", include("service.urls")),
    # path('verification/', include('verify_email.urls')),
    path("accounts/", include("allauth.urls")),
    path("", include("django.contrib.auth.urls")),
    path("user_center/", include("user_center.urls")),
    path("forum/", include("forum.urls")),
    path("admin_system/", include("admin_system.urls")),
]

handler404 = "basic.views.handle_not_found"
# handler500= "basic.views.handle_not_found"
