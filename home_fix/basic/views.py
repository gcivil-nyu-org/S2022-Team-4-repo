from django.shortcuts import render


# Homepage
def homepage_view(request):
    return render(request, "basic/homepage.html")
