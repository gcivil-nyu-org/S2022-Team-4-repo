# Generated by Django 4.0 on 2022-05-10 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_alter_customuser_coin_alter_customuser_tier"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_frozen",
            field=models.BooleanField(default=False),
        ),
    ]
