# Generated by Django 4.2.8 on 2024-01-03 18:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("request_logs", "0015_squashed"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="httplog",
            name="request_log_tickete_abc69b_idx",
        ),
        migrations.RemoveField(
            model_name="httplog",
            name="ticketer",
        ),
    ]
