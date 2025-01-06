# Generated by Django 5.1.4 on 2025-01-06 21:25

import django.contrib.postgres.fields
import django.utils.timezone
from django.db import migrations, models

import temba.orgs.models
import temba.utils.fields
import temba.utils.models.fields
import temba.utils.uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contacts", "0197_squashed"),
    ]

    operations = [
        migrations.CreateModel(
            name="BroadcastMsgCount",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                ("count", models.IntegerField()),
                ("is_squashed", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Label",
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
                ("uuid", models.UUIDField(default=temba.utils.uuid.uuid4, unique=True)),
                (
                    "name",
                    models.CharField(max_length=64, validators=[temba.utils.fields.NameValidator(64)]),
                ),
                ("is_system", models.BooleanField(default=False)),
            ],
            bases=(models.Model, temba.orgs.models.DependencyMixin),
        ),
        migrations.CreateModel(
            name="LabelCount",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                ("count", models.IntegerField()),
                ("is_squashed", models.BooleanField(default=False)),
                ("is_archived", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Media",
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
                ("uuid", models.UUIDField(default=temba.utils.uuid.uuid4, unique=True)),
                ("url", models.URLField(max_length=2048)),
                ("content_type", models.CharField(max_length=255)),
                ("path", models.CharField(max_length=2048)),
                ("size", models.IntegerField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[("P", "Pending"), ("R", "Ready"), ("F", "Failed")],
                        default="P",
                        max_length=1,
                    ),
                ),
                ("duration", models.IntegerField(default=0)),
                ("width", models.IntegerField(default=0)),
                ("height", models.IntegerField(default=0)),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Msg",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("uuid", models.UUIDField(default=temba.utils.uuid.uuid4)),
                ("text", models.TextField()),
                (
                    "attachments",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.URLField(max_length=2048),
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "quick_replies",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=64), null=True, size=None
                    ),
                ),
                ("locale", models.CharField(max_length=6, null=True)),
                ("templating", models.JSONField(null=True)),
                ("created_on", models.DateTimeField(db_index=True)),
                ("modified_on", models.DateTimeField()),
                ("sent_on", models.DateTimeField(null=True)),
                (
                    "msg_type",
                    models.CharField(
                        choices=[
                            ("T", "Text"),
                            ("O", "Opt-In Request"),
                            ("V", "Interactive Voice Response"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "direction",
                    models.CharField(choices=[("I", "Incoming"), ("O", "Outgoing")], max_length=1),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "Pending"),
                            ("H", "Handled"),
                            ("I", "Initializing"),
                            ("Q", "Queued"),
                            ("W", "Wired"),
                            ("S", "Sent"),
                            ("D", "Delivered"),
                            ("R", "Read"),
                            ("E", "Error"),
                            ("F", "Failed"),
                        ],
                        db_index=True,
                        default="P",
                        max_length=1,
                    ),
                ),
                (
                    "visibility",
                    models.CharField(
                        choices=[
                            ("V", "Visible"),
                            ("A", "Archived"),
                            ("D", "Deleted by user"),
                            ("X", "Deleted by sender"),
                        ],
                        default="V",
                        max_length=1,
                    ),
                ),
                ("is_android", models.BooleanField(null=True)),
                ("msg_count", models.IntegerField(default=1)),
                ("high_priority", models.BooleanField(null=True)),
                ("error_count", models.IntegerField(default=0)),
                ("next_attempt", models.DateTimeField(null=True)),
                (
                    "failed_reason",
                    models.CharField(
                        choices=[
                            ("S", "Workspace suspended"),
                            ("C", "Contact is no longer active"),
                            ("L", "Looping detected"),
                            ("E", "Retry limit reached"),
                            ("O", "Too old to send"),
                            ("D", "No suitable channel found"),
                            ("R", "Channel removed"),
                        ],
                        max_length=1,
                        null=True,
                    ),
                ),
                ("external_id", models.CharField(max_length=255, null=True)),
                (
                    "log_uuids",
                    django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(), null=True, size=None),
                ),
                (
                    "metadata",
                    temba.utils.models.fields.JSONAsTextField(default=dict, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OptIn",
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
                ("uuid", models.UUIDField(default=temba.utils.uuid.uuid4, unique=True)),
                (
                    "name",
                    models.CharField(max_length=64, validators=[temba.utils.fields.NameValidator(64)]),
                ),
                ("is_system", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="SystemLabelCount",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                ("count", models.IntegerField()),
                ("is_squashed", models.BooleanField(default=False)),
                (
                    "label_type",
                    models.CharField(
                        choices=[
                            ("I", "Inbox"),
                            ("W", "Flows"),
                            ("A", "Archived"),
                            ("O", "Outbox"),
                            ("S", "Sent"),
                            ("X", "Failed"),
                            ("E", "Scheduled"),
                            ("C", "Calls"),
                        ],
                        max_length=1,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Broadcast",
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
                        choices=[
                            ("P", "Pending"),
                            ("Q", "Queued"),
                            ("S", "Started"),
                            ("C", "Completed"),
                            ("F", "Failed"),
                            ("I", "Interrupted"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
                ("contact_count", models.IntegerField(default=0, null=True)),
                (
                    "urns",
                    django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), null=True, size=None),
                ),
                ("query", models.TextField(null=True)),
                ("node_uuid", models.UUIDField(null=True)),
                ("exclusions", models.JSONField(default=dict, null=True)),
                ("translations", models.JSONField()),
                ("base_language", models.CharField(max_length=3)),
                (
                    "template_variables",
                    django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), null=True, size=None),
                ),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "modified_on",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("is_active", models.BooleanField(default=True, null=True)),
                (
                    "contacts",
                    models.ManyToManyField(related_name="addressed_broadcasts", to="contacts.contact"),
                ),
            ],
        ),
    ]
