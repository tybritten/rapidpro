# Generated by Django 5.1.4 on 2025-02-19 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("channels", "0193_channel_is_enabled"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channel",
            name="is_enabled",
            field=models.BooleanField(
                default=True,
                help_text="Makes channel available for sending. Incoming messages will be received regardless.",
            ),
        ),
    ]
