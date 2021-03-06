# Generated by Django 4.0 on 2022-03-30 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Services",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "service_category",
                    models.CharField(
                        blank=True, max_length=128, verbose_name="service category"
                    ),
                ),
                (
                    "service_description",
                    models.TextField(blank=True, verbose_name="service_description"),
                ),
                (
                    "coins_charged",
                    models.IntegerField(default=0, verbose_name="coins_charged"),
                ),
                (
                    "street",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="street"
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="state"
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="country"
                    ),
                ),
                (
                    "zip",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="zip"
                    ),
                ),
                (
                    "long",
                    models.DecimalField(
                        blank=True,
                        decimal_places=16,
                        max_digits=22,
                        null=True,
                        verbose_name="longitude",
                    ),
                ),
                (
                    "lat",
                    models.DecimalField(
                        blank=True,
                        decimal_places=16,
                        max_digits=22,
                        null=True,
                        verbose_name="latitude",
                    ),
                ),
                (
                    "provider_email",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.customuser",
                    ),
                ),
            ],
        ),
    ]
