import stripe

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user_center.models import Transaction
from .forms import CustomUserCreationForm, LocationForm, CustomUserChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from .models import CustomUser, Product
from home_fix.settings import EMAIL_HOST_USER

stripe.api_key = settings.STRIPE_SECRET_KEY
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
            return redirect("basic:index")
        return render(request, "users/register.html", {"form": form})


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect("basic:index")
    if request.method == "POST":
        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("basic:index")
        else:
            err = "Username or password is incorrect"
            return render(request, "users/login.html", {"error": err})

    return render(request, "users/login.html")


#   Set location
def set_location(request, user_id):
    context = {"user_id": user_id}
    if request.method == "POST":
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
            return redirect("basic:index")
    else:
        # re = request
        # if request.user.id == int(form.data.get("id")) and request.user.is_authenticated:
        return render(request, "users/set_location.html", context)


# Pricing
def pricing_view(request):
    if not request.user.is_authenticated:
        return redirect("basic:index")
    if request.method == "POST":
        try:
            tier = int(request.POST.get("tier"))
        except ValueError:
            return redirect("basic:index")
        if tier not in [1]:
            # wrong params
            return redirect("basic:index")
        else:
            user = CustomUser.objects.get(id=request.user.id)
            user.tier = tier
            user.save()
            return redirect("basic:index")
    else:
        product1 = Product.objects.get(tier=1)
        product2 = Product.objects.get(tier=2)
        product3 = Product.objects.get(tier=3)

        return render(
            request,
            "users/pricing.html",
            {
                "product1": product1,
                "product2": product2,
                "product3": product3,
                "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
            },
        )


# Stripe Checkout Backend
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_tier = self.kwargs["pk"]
        product = Product.objects.get(tier=product_tier)
        # YOUR_DOMAIN = "http://127.0.0.1:8000/"
        if request.is_secure():
            YOUR_DOMAIN = "".join([get_current_site(request).domain])
        else:
            YOUR_DOMAIN = "".join(["http://", get_current_site(request).domain])
        unit_price = int(float(product.price) * 100)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": unit_price,
                        "product_data": {
                            "name": product.name,
                            # 'images': [
                            #     'https://images.unsplash.com/20/cambridge.JPG?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1030&q=80'],
                        },
                    },
                    "quantity": 1,
                    "tax_rates": ["txr_1Ki0PYHgOFOjKM17qZ1TP5Um"],
                },
            ],
            metadata={
                "product_tier": product_tier,
                "product_name": product.name,
                "user_id": request.user.id,
            },
            mode="payment",
            # discounts=[{
            #     'coupon': 'lpnrN54N',
            # }],
            allow_promotion_codes=True,
            success_url=YOUR_DOMAIN,
            if request.is_secure():
                cancel_url=YOUR_DOMAIN + "/users/pricing/",
            else:
                cancel_url=YOUR_DOMAIN + "users/pricing/",
        )
        return JsonResponse({"id": checkout_session.id})


# Payment Success
def success_view(request):
    return render(request, "users/success.html")


# Payment Cancelled
def cancel_view(request):
    return render(request, "users/cancel.html")


# Stripe webhook
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Fulfill the purchase...
        User = get_user_model()
        user_id = session["metadata"]["user_id"]
        user = User.objects.get(id=user_id)
        product_name = session["metadata"]["product_name"]
        user.tier = int(session["metadata"]["product_tier"])
        product = Product.objects.get(product_name=product_name)
        print(f"User tier: {user.tier}")
        user.save()
        Transaction.objects.create(
            sender=EMAIL_HOST_USER,
            receiver=user.email,
            amount=product.price,
            service_type="membership fee",
        )
        user.coin += product.price
        user.save()

    # Passed signature verification
    return HttpResponse(status=200)


# Logout
def logout_view(request):
    logout(request)
    # messages.info(request, "You have successfully logged out.")
    return redirect("basic:index")


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
        # return redirect('users')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect("users:set_location", user_id=user.id)
    else:
        return HttpResponse("Activation link is invalid!")


def actilink(request):
    return HttpResponse("Please Verify your Email!!")


def profile_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        user.password = None
        return render(request, "users/profile.html", context={"user": user})
    else:
        return redirect("basic:index")


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
        return redirect("basic:index")
