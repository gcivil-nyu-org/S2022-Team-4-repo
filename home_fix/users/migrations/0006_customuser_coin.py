# Generated by Django 4.0 on 2022-04-03 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="coin",
            field=models.IntegerField(default=0),
        ),
    ]
