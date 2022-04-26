from django.shortcuts import render


# Homepage
def homepage_view(request):
    return render(request, "basic/homepage.html")


def handle_not_found(request, exception):
    return render(request, "basic/notfound.html")
