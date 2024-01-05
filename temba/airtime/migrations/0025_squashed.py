# Generated by Django 4.2.8 on 2024-01-05 15:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="AirtimeTransfer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("S", "Success"), ("F", "Failed")], max_length=1
                    ),
                ),
                ("recipient", models.CharField(max_length=255)),
                ("sender", models.CharField(max_length=255, null=True)),
                ("currency", models.CharField(max_length=32, null=True)),
                (
                    "desired_amount",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("actual_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
