from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    #  delete username file
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=128, blank=True)
    last_name = models.CharField('last name', max_length=128, blank=True)
    gender = models.CharField('gen.scder', max_length=32, blank=True)
    location = models.CharField('location', max_length=128, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    # set email as primary key
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        # return self.user.__str__()
        return "{}".format(self.email.__str__())
