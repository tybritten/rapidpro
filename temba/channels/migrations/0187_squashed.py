# Generated by Django 5.1.4 on 2025-01-06 21:25

import uuid

import django_countries.fields

import django.contrib.postgres.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import temba.channels.models
import temba.orgs.models
import temba.utils.models.base
import temba.utils.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ChannelCount",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                ("count", models.IntegerField()),
                ("is_squashed", models.BooleanField(default=False)),
                (
                    "count_type",
                    models.CharField(
                        choices=[
                            ("IM", "Incoming Message"),
                            ("OM", "Outgoing Message"),
                            ("IV", "Incoming Voice"),
                            ("OV", "Outgoing Voice"),
                            ("LS", "Success Log Record"),
                            ("LE", "Error Log Record"),
                        ],
                        max_length=2,
                    ),
                ),
                ("day", models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ChannelEvent",
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
                    "event_type",
                    models.CharField(
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
                        ],
                        max_length=16,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("P", "Pending"), ("H", "Handled")],
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "extra",
                    temba.utils.models.fields.JSONAsTextField(default=dict, null=True),
                ),
                ("occurred_on", models.DateTimeField()),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "log_uuids",
                    django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), null=True, size=None),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChannelLog",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4)),
                (
                    "log_type",
                    models.CharField(
                        choices=[
                            ("unknown", "Other Event"),
                            ("msg_send", "Message Send"),
                            ("msg_status", "Message Status"),
                            ("msg_receive", "Message Receive"),
                            ("event_receive", "Event Receive"),
                            ("multi_receive", "Events Receive"),
                            ("ivr_start", "IVR Start"),
                            ("ivr_incoming", "IVR Incoming"),
                            ("ivr_callback", "IVR Callback"),
                            ("ivr_status", "IVR Status"),
                            ("ivr_hangup", "IVR Hangup"),
                            ("attachment_fetch", "Attachment Fetch"),
                            ("token_refresh", "Token Refresh"),
                            ("page_subscribe", "Page Subscribe"),
                            ("webhook_verify", "Webhook Verify"),
                        ],
                        max_length=16,
                    ),
                ),
                ("http_logs", models.JSONField(null=True)),
                ("errors", models.JSONField(null=True)),
                ("is_error", models.BooleanField(default=False)),
                ("elapsed_ms", models.IntegerField(default=0)),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="SyncEvent",
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
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Whether this item is active, use this instead of deleting",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        help_text="When this item was originally created",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        help_text="When this item was last modified",
                    ),
                ),
                (
                    "power_source",
                    models.CharField(
                        choices=[
                            ("AC", "A/C"),
                            ("USB", "USB"),
                            ("WIR", "Wireless"),
                            ("BAT", "Battery"),
                        ],
                        max_length=64,
                    ),
                ),
                (
                    "power_status",
                    models.CharField(
                        choices=[
                            ("UNK", "Unknown"),
                            ("CHA", "Charging"),
                            ("DIS", "Discharging"),
                            ("NOT", "Not Charging"),
                            ("FUL", "FUL"),
                        ],
                        default="UNK",
                        max_length=64,
                    ),
                ),
                ("power_level", models.IntegerField()),
                ("network_type", models.CharField(max_length=128)),
                ("lifetime", models.IntegerField(blank=True, default=0, null=True)),
                ("pending_message_count", models.IntegerField(default=0)),
                ("retry_message_count", models.IntegerField(default=0)),
                ("incoming_command_count", models.IntegerField(default=0)),
                ("outgoing_command_count", models.IntegerField(default=0)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Channel",
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
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Whether this item is active, use this instead of deleting",
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        help_text="When this item was originally created",
                    ),
                ),
                (
                    "modified_on",
                    models.DateTimeField(
                        blank=True,
                        default=django.utils.timezone.now,
                        editable=False,
                        help_text="When this item was last modified",
                    ),
                ),
                (
                    "uuid",
                    models.CharField(
                        db_index=True,
                        default=temba.utils.models.base.generate_uuid,
                        help_text="The unique identifier for this object",
                        max_length=36,
                        unique=True,
                        verbose_name="Unique Identifier",
                    ),
                ),
                ("is_system", models.BooleanField(default=False)),
                ("channel_type", models.CharField(max_length=3)),
                ("name", models.CharField(max_length=64)),
                (
                    "address",
                    models.CharField(
                        blank=True,
                        help_text="Address with which this channel communicates",
                        max_length=255,
                        null=True,
                        verbose_name="Address",
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        blank=True,
                        help_text="Country which this channel is for",
                        max_length=2,
                        null=True,
                        verbose_name="Country",
                    ),
                ),
                ("config", models.JSONField(default=dict)),
                (
                    "schemes",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=16),
                        default=temba.channels.models._get_default_channel_scheme,
                        size=None,
                    ),
                ),
                ("role", models.CharField(default="SR", max_length=4)),
                (
                    "log_policy",
                    models.CharField(
                        choices=[
                            ("N", "Discard All"),
                            ("E", "Write Errors Only"),
                            ("A", "Write All"),
                        ],
                        default="A",
                        max_length=1,
                    ),
                ),
                ("tps", models.IntegerField(null=True)),
                (
                    "claim_code",
                    models.CharField(blank=True, max_length=16, null=True, unique=True),
                ),
                (
                    "secret",
                    models.CharField(blank=True, max_length=64, null=True, unique=True),
                ),
                ("device", models.CharField(blank=True, max_length=255, null=True)),
                ("os", models.CharField(blank=True, max_length=255, null=True)),
                ("last_seen", models.DateTimeField(null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="The user which originally created this item",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(app_label)s_%(class)s_creations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        help_text="The user which last modified this item",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(app_label)s_%(class)s_modifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-last_seen", "-pk"),
            },
            bases=(models.Model, temba.orgs.models.DependencyMixin),
        ),
    ]
