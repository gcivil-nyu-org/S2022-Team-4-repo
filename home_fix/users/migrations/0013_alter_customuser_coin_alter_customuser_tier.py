# Generated by Django 4.0 on 2022-04-27 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_customuser_profile_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="coin",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=20, null=True
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="tier",
            field=models.IntegerField(default=-1),
        ),
    ]
