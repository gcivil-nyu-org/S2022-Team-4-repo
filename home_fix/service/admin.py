from django.contrib import admin

# Register your models here.
from service.models import Order, Services

admin.site.register(Order)
admin.site.register(Services)
