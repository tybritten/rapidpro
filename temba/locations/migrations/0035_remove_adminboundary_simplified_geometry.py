# Generated by Django 5.1.4 on 2025-01-10 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0034_populate_json_geometry"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="adminboundary",
            name="simplified_geometry",
        ),
    ]
