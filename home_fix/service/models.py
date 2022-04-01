from django.db import models

# Create your models here.
from users.models import CustomUser


class Services(models.Model):
    service_category = models.CharField("service category", max_length=128, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service_description = models.TextField("service_description", blank=True)
    coins_charged = models.IntegerField("coins_charged", default=0)
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

    def _str_(self):
        return "{}".format(self.service_category._str_())
