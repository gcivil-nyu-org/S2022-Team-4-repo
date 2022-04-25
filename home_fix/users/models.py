from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.
from .managers import CustomUserManager


# from home_fix.settings import EMAIL_HOST_USER


class CustomUser(AbstractBaseUser, PermissionsMixin):
    #  delete username file
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField("first name", max_length=128, blank=True)
    last_name = models.CharField("last name", max_length=128, blank=True)
    gender = models.CharField("gender", max_length=32, blank=True)
    street = models.CharField("street", max_length=64, blank=True, null=True)
    state = models.CharField("state", max_length=64, blank=True, null=True)
    country = models.CharField("country", max_length=64, blank=True, null=True)
    zip = models.CharField("zip", max_length=64, blank=True, null=True)
    long = models.DecimalField(
        "longitude", max_digits=22, decimal_places=16, blank=True, null=True
    )
    lat = models.DecimalField(
        "latitude", max_digits=22, decimal_places=16, blank=True, null=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    tier = models.IntegerField(default=1)
    coin = models.DecimalField(
        max_digits=20, decimal_places=2, default=100, blank=True, null=True
    )
    # coins = models.IntegerField(default=0)
    # set email as primary key
    USERNAME_FIELD = "email"
    objects = CustomUserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        # return self.user.__str__()
        return "{}".format(self.email.__str__())


class Product(models.Model):
    tier = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        "price",
        max_digits=20,
        decimal_places=2,
        default=0.0,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    # def get_display_price(self):  # diplay price in dollars
    #     return "{0:.2f}".format(self.price / 100)


class LoginRecord(models.Model):
    ip = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
