from atexit import register
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LocationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import logging
from django.contrib.auth import get_user_model
import json
# Create your views here.
from .models import CustomUser

def auth(request):
    return HttpResponseRedirect(reverse("authentication:index"))


# Regitration / Sign Up
def register_view(request):
    logging.warning(request.POST)
    print(request)
    if request.method == "POST":
        logging.warning("First")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            #login(request, user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your HomeFix account.'
            message = render_to_string('authentication/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect ("authentication:activationlinkpage")
            #return render(request, "authentication/activation_link_sent.html")
#             logging.warning("Second")
#             user = form.save()
#             login(request, user)
#             return redirect("authentication:set_location", user_id=user.id)
        else:
            # can show up message
            logging.warning("Third")
            return render(request, "authentication/register.html", {"form": form})
    else:
        logging.warning("Fourth")
        form = CustomUserCreationForm()
        logging.warning(request.user)
        if request.user.is_authenticated and request.user.country==None:
            return redirect("authentication:set_location", user_id=request.user.id)
        if request.user.is_authenticated and request.user.country:
            return redirect("authentication:index")
        return render(request, "authentication/register.html", {"form": form})


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect("authentication:index")
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("authentication:index")
        else:
            err = "Username or password is incorrect"
            return render(request, "authentication/login.html", {"error": err})

    return render(request, "authentication/login.html")


#   Set location
def set_location(request, user_id):
    context = {"user_id": user_id}
    if request.method == "POST":
        if request.user.id == user_id and request.user.is_authenticated:
            form = LocationForm(request.POST, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                print(user)
                user.save()
                return redirect("authentication:pricing")
            else:
                # add alert in future
                render(request, "authentication/set_location.html")
        #   illegal request. this user should not visit this page
        else:
            logout(request)
            redirect("authentication:index")
    else:
        re = request
        # if request.user.id == int(form.data.get("id")) and request.user.is_authenticated:
        return render(request, "authentication/set_location.html", context)


# Pricing
def pricing_view(request):
    if not request.user.is_authenticated:
        return redirect("authentication:index")
    if request.method == "POST":
        tier = int(request.POST.get("tier"))
        if tier not in [0, 1, 2]:
            # wrong params
            return render(request, "authentication/pricing.html")
        else:
            user = CustomUser.objects.get(id=request.user.id)
            user.tier = tier
            user.save()
            return redirect("authentication:index")
    else:
        return render(request, "authentication/pricing.html")


# Homepage
def homepage_view(request):
    return render(request, "authentication/homepage.html")


# Logout
def logout_view(request):
    logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect("authentication:index")

# Email Verification

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect("authentication:set_location", user_id=user.id)
    else:
        return HttpResponse('Activation link is invalid!')
def actilink(request):
    return HttpResponse("Please Verify your Email!!")

def search(request):
    User = get_user_model()
    users = User.objects.all()
    locations=[]
    for i in users:
        temp=[]
        if(i.lat==None or i.long==None):
            continue
        temp.append(float(i.lat))
        temp.append(float(i.long))
        locations.append(temp)

    return render(request,'authentication/locs.html',context={'users':locations})