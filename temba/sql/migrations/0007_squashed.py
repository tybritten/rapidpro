# Generated by Django 5.1.4 on 2025-01-06 21:25

from django.db import migrations

from . import InstallSQL


class Migration(migrations.Migration):

    dependencies = [
        ("notifications", "0031_squashed"),
        ("ivr", "0031_squashed"),
        ("locations", "0032_squashed"),
        ("msgs", "0282_squashed"),
        ("orgs", "0163_squashed"),
        ("tickets", "0074_squashed"),
    ]

    operations = [InstallSQL("0007_functions"), InstallSQL("0007_triggers")]
