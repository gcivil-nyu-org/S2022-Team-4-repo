from django.db import models

# Create your models here.
from service.models import Services
from users.models import CustomUser
import django.db.models.deletion


class Report(models.Model):
    service = models.ForeignKey(Services, on_delete=django.db.models.deletion.CASCADE)
    reporter = models.ForeignKey(
        CustomUser, on_delete=django.db.models.deletion.CASCADE
    )
    content = models.TextField("content", blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField("status", max_length=32, blank=True, default="unsolved")
