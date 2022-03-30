import stripe
import logging
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LocationForm, CustomUserChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import CustomUser

stripe.api_key = settings.STRIPE_SECRET_KEY
# stripe.Coupon.create(percent_off=20, duration="once")
stripe.TaxRate.create(
    display_name="Sales Tax",
    inclusive=False,
    percentage=7.25,
    country="US",
    state="NY",
    jurisdiction="US - NY",
    description="NY Sales Tax",
)


# Create your views here.


# def auth(request):
#     return HttpResponseRedirect(reverse("users:index"))


# Regitration / Sign Up
def register_view(request):
    # logging.warning(request.POST)
    if request.method == "POST":
        # logging.warning("First")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # login(request, user)
            current_site = get_current_site(request)
            mail_subject = "Activate your HomeFix account."
            message = render_to_string(
                "users/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect("users:activationlinkpage")
        else:
            # can show up message
            # logging.warning("Third")
            return render(request, "users/register.html", {"form": form})
    else:
        # logging.warning("Fourth")
        form = CustomUserCreationForm()
        # logging.warning(request.user)
        if request.user.is_authenticated and request.user.country is None:
            return redirect("users:set_location", user_id=request.user.id)
        if request.user.is_authenticated and request.user.country:
            return redirect("users:index")
        return render(request, "users/register.html", {"form": form})


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect("users:index")
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("users:index")
        else:
            err = "Username or password is incorrect"
            return render(request, "users/login.html", {"error": err})

    return render(request, "users/login.html")


#   Set location
def set_location(request, user_id):
    context = {"user_id": user_id}
    if request.method == "POST":
        print(request.user)
        if request.user.id == user_id and request.user.is_authenticated:
            form = LocationForm(request.POST, instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                return redirect("users:pricing")
            else:
                # add alert in future
                return render(request, "users/set_location.html", context)
        #   illegal request. this user should not visit this page
        else:
            logout(request)
            return redirect("users:index")
    else:
        # re = request
        # if request.user.id == int(form.data.get("id")) and request.user.is_authenticated:
        return render(request, "users/set_location.html", context)


# Pricing
def pricing_view(request):
    if not request.user.is_authenticated:
        return redirect("users:index")
    if request.method == "POST":
        try:
            tier = int(request.POST.get("tier"))
        except ValueError:
            return render(request, "users/pricing.html")
        if tier not in [0, 1, 2]:
            # wrong params
            return render(request, "users/pricing.html")
        else:
            user = CustomUser.objects.get(id=request.user.id)
            user.tier = tier
            user.save()
            return redirect("users:index")
    else:
        return render(request, "users/pricing.html")


# Stripe Integration
# class CreateCheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=["card"],
#             line_items=[
#                 {
#                     "price_data": {
#                         "currency": "usd",
#                         "unit_amount": 10000,
#                         "product_data": {
#                             "name": "Starter Pack",
#                             # 'images': [
#                             #     'https://images.unsplash.com/20/cambridge.JPG?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1030&q=80'],
#                         },
#                     },
#                     "quantity": 1,
#                     "tax_rates": ["txr_1Ki0PYHgOFOjKM17qZ1TP5Um"],
#                 },
#             ],
#             mode="payment",
#             # discounts=[{
#             #     'coupon': 'lpnrN54N',
#             # }],
#             allow_promotion_codes=True,
#             # success_url= 'http://127.0.0.1:8000/',
#             success_url="https://homefix-dev.herokuapp.com/",
#             # cancel_url='http://127.0.0.1:8000/pricing',
#             cancel_url="https://homefix-dev.herokuapp.com/pricing",
#         )
#         return JsonResponse({"id": checkout_session.id})


# Homepage
def homepage_view(request):
    return render(request, "users/homepage.html")


# Logout
def logout_view(request):
    logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect("users:index")


# Email Verification


def activate(
    request, uidb64, token, backend="django.contrib.auth.backends.ModelBackend"
):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect("users:set_location", user_id=user.id)
    else:
        return HttpResponse("Activation link is invalid!")


def actilink(request):
    return HttpResponse("Please Verify your Email!!")


def search(request):
    if not request.user.is_authenticated:
        return redirect("users:login")
    User = get_user_model()
    users = User.objects.all()
    userloc = []
    userloc.append(float(request.user.lat))
    userloc.append(float(request.user.long))
    locations = []
    for i in users:
        temp = []
        if i.lat is None or i.long is None:
            print(i)
            continue
        temp.append(float(i.lat))
        temp.append(float(i.long))
        locations.append(temp)

    return render(
        request,
        "users/locs.html",
        context={
            "users": locations,
            "user": userloc,
        },
    )


def search_hardware(request):
    if not request.user.is_authenticated:
        return redirect("users:login")
    User = get_user_model()
    users = User.objects.all()
    locations = []
    for i in users:
        temp = []
        if i.lat is None or i.long is None:
            print(i)
            continue
        temp.append(float(i.lat))
        temp.append(float(i.long))
        locations.append(temp)
    userloc = []
    userloc.append(float(request.user.lat))
    userloc.append(float(request.user.long))

    return render(
        request,
        "users/locs_hardware.html",
        context={"users": locations, "user": userloc},
    )


def profile_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user.password = None
        return render(request, "users/profile.html", context={"user": user})
    else:
        return redirect("users:index")


def profile_editor_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user.password = None
        if request.method == "POST":
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
            return redirect("users:profile")
        else:
            return render(request, "users/profile_editor.html", context={"user": user})
    else:
        return redirect("users:index")


def request_service_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user.password = None
        return render(request, "users/request_services.html", context={"user": user})
    else:
        return redirect("users:index")


def offer_service_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user.password = None
        return render(request, "users/offer_services.html", context={"user": user})
    else:
        return redirect("users:index")
