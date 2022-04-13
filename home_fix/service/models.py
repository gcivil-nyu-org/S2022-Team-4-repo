from django.db import models

# Create your models here.
from user_center.models import Transaction
from users.models import CustomUser


class Services(models.Model):
    service_category = models.CharField("service category", max_length=128, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_description = models.TextField("service_description", blank=True)
    coins_charged = models.DecimalField(
        "coins_charged",
        max_digits=20,
        decimal_places=2,
        default=0.0,
        blank=True,
        null=True,
    )
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
    # can hide post by setting visible as false
    visible = models.BooleanField("visible", default=True, blank=True)
    # time
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.service_category.__str__())


# when a user take a service, it will create an order
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        "status", max_length=64, blank=True, null=True, default="pending"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    # status : pending / cancel/ in progress / finished
    #
    def __str__(self):
        return "{} {}".format(self.service.__str__(), self.user.__str__())


class Notifications(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=64)
    read = models.IntegerField(default=0)
