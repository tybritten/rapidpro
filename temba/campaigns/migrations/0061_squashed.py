# Generated by Django 5.1.4 on 2025-01-06 21:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.contrib.postgres.operations import HStoreExtension
from django.db import migrations, models

import temba.utils.fields
import temba.utils.models.fields
import temba.utils.uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        HStoreExtension(),
        migrations.CreateModel(
            name="CampaignEvent",
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
                    "event_type",
                    models.CharField(
                        choices=[("F", "Flow Event"), ("M", "Message Event")],
                        default="F",
                        max_length=1,
                    ),
                ),
                ("offset", models.IntegerField(default=0)),
                (
                    "unit",
                    models.CharField(
                        choices=[
                            ("M", "Minutes"),
                            ("H", "Hours"),
                            ("D", "Days"),
                            ("W", "Weeks"),
                        ],
                        default="D",
                        max_length=1,
                    ),
                ),
                (
                    "start_mode",
                    models.CharField(
                        choices=[("I", "Interrupt"), ("S", "Skip"), ("P", "Passive")],
                        default="I",
                        max_length=1,
                    ),
                ),
                (
                    "message",
                    temba.utils.models.fields.TranslatableField(max_length=640, null=True),
                ),
                ("delivery_hour", models.IntegerField(default=-1)),
            ],
            options={
                "verbose_name": "Campaign Event",
                "verbose_name_plural": "Campaign Events",
            },
        ),
        migrations.CreateModel(
            name="EventFire",
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
                ("scheduled", models.DateTimeField()),
                ("fired", models.DateTimeField(null=True)),
                (
                    "fired_result",
                    models.CharField(
                        choices=[("F", "Fired"), ("S", "Skipped")],
                        max_length=1,
                        null=True,
                    ),
                ),
            ],
            options={
                "ordering": ("scheduled",),
            },
        ),
        migrations.CreateModel(
            name="Campaign",
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
                ("is_archived", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="The user which originally created this item",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(app_label)s_%(class)s_creations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Campaign",
                "verbose_name_plural": "Campaigns",
            },
        ),
    ]
