# Generated by Django 4.2.8 on 2024-03-11 21:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0021_alter_incident_incident_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="contact_export",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="message_export",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="results_export",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="ticket_export",
        ),
    ]
