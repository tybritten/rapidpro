# Generated by Django 5.1.4 on 2025-02-12 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("channels", "0188_squashed"),
    ]

    operations = [
        migrations.AddField(
            model_name="channelevent",
            name="uuid",
            field=models.UUIDField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="channelevent",
            name="event_type",
            field=models.CharField(
                choices=[
                    ("mt_call", "Outgoing Call"),
                    ("mt_miss", "Missed Outgoing Call"),
                    ("mo_call", "Incoming Call"),
                    ("mo_miss", "Missed Incoming Call"),
                    ("stop_contact", "Stop Contact"),
                    ("new_conversation", "New Conversation"),
                    ("referral", "Referral"),
                    ("welcome_message", "Welcome Message"),
                    ("optin", "Opt In"),
                    ("optout", "Opt Out"),
                    ("delete_contact", "Delete Contact"),
                ],
                max_length=16,
            ),
        ),
    ]
