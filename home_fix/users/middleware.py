from django.shortcuts import render, redirect
from django.contrib.auth import logout


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated and request.user.is_frozen:
            logout(request)
            err = (
                "Your Account has been blocked, please contact admin homefix@gmail.com"
            )
            return redirect("users:login_error", {"err": err})
        response = get_response(request)
        return response

    return middleware
