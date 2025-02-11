# Generated by Django 5.1.4 on 2025-01-06 21:25

import pyotp
import storages.backends.s3
import timezone_field.fields

import django.contrib.auth.models
import django.contrib.postgres.fields
import django.contrib.postgres.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import temba.orgs.models
import temba.utils.fields
import temba.utils.json
import temba.utils.models.fields
import temba.utils.text
import temba.utils.uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BackupToken",
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
                    "token",
                    models.CharField(
                        default=temba.utils.text.generate_token,
                        max_length=18,
                        unique=True,
                    ),
                ),
                ("is_used", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="Export",
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
                ("export_type", models.CharField(max_length=20)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "Pending"),
                            ("O", "Processing"),
                            ("C", "Complete"),
                            ("F", "Failed"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
                ("num_records", models.IntegerField(null=True)),
                ("path", models.CharField(max_length=2048, null=True)),
                ("start_date", models.DateField(null=True)),
                ("end_date", models.DateField(null=True)),
                ("config", models.JSONField(default=dict)),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "modified_on",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ItemCount",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
                ),
                ("count", models.IntegerField()),
                ("is_squashed", models.BooleanField(default=False)),
                ("scope", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Org",
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
                ("name", models.CharField(max_length=128, verbose_name="Name")),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("en-us", "English"),
                            ("cs", "Czech"),
                            ("es", "Spanish"),
                            ("fr", "French"),
                            ("mn", "Mongolian"),
                            ("pt-br", "Portuguese"),
                            ("ru", "Russian"),
                        ],
                        default="en-us",
                        help_text="Default website language for new users.",
                        max_length=64,
                        null=True,
                        verbose_name="Default Language",
                    ),
                ),
                (
                    "timezone",
                    timezone_field.fields.TimeZoneField(verbose_name="Timezone"),
                ),
                (
                    "date_format",
                    models.CharField(
                        choices=[
                            ("D", "DD-MM-YYYY"),
                            ("M", "MM-DD-YYYY"),
                            ("Y", "YYYY-MM-DD"),
                        ],
                        default="D",
                        help_text="Default formatting and parsing of dates in flows and messages.",
                        max_length=1,
                        verbose_name="Date Format",
                    ),
                ),
                (
                    "flow_languages",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=3),
                        default=list,
                        size=None,
                        validators=[django.contrib.postgres.validators.ArrayMinLengthValidator(1)],
                    ),
                ),
                (
                    "input_collation",
                    models.CharField(
                        choices=[
                            ("default", "Case insensitive (e.g. A = a)"),
                            (
                                "confusables",
                                "Visually similiar characters (e.g. 𝓐 = A = a = ⍺)",
                            ),
                            (
                                "arabic_variants",
                                "Arabic, Farsi and Pashto equivalents (e.g. ي = ی = ۍ)",
                            ),
                        ],
                        default="default",
                        max_length=32,
                    ),
                ),
                ("flow_smtp", models.CharField(null=True)),
                ("prometheus_token", models.CharField(max_length=40, null=True)),
                ("config", models.JSONField(default=dict)),
                (
                    "slug",
                    models.SlugField(
                        blank=True,
                        error_messages={"unique": "This slug is not available"},
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="Slug",
                    ),
                ),
                (
                    "features",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=32),
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "limits",
                    temba.utils.models.fields.JSONField(
                        decoder=temba.utils.json.TembaDecoder,
                        default=dict,
                        encoder=temba.utils.json.TembaEncoder,
                    ),
                ),
                (
                    "api_rates",
                    temba.utils.models.fields.JSONField(
                        decoder=temba.utils.json.TembaDecoder,
                        default=dict,
                        encoder=temba.utils.json.TembaEncoder,
                    ),
                ),
                (
                    "is_anon",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this organization anonymizes the phone numbers of contacts within it",
                    ),
                ),
                (
                    "is_flagged",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this organization is currently flagged.",
                    ),
                ),
                (
                    "is_suspended",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this organization is currently suspended.",
                    ),
                ),
                ("suspended_on", models.DateTimeField(null=True)),
                ("released_on", models.DateTimeField(null=True)),
                ("deleted_on", models.DateTimeField(null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OrgImport",
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
                    "file",
                    models.FileField(upload_to=temba.orgs.models.get_import_upload_path),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "Pending"),
                            ("O", "Processing"),
                            ("C", "Complete"),
                            ("F", "Failed"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OrgMembership",
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
                ("role_code", models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name="UserSettings",
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
                    "language",
                    models.CharField(
                        choices=[
                            ("en-us", "English"),
                            ("cs", "Czech"),
                            ("es", "Spanish"),
                            ("fr", "French"),
                            ("mn", "Mongolian"),
                            ("pt-br", "Portuguese"),
                            ("ru", "Russian"),
                        ],
                        default="en-us",
                        max_length=8,
                    ),
                ),
                (
                    "otp_secret",
                    models.CharField(default=pyotp.random_base32, max_length=16),
                ),
                ("two_factor_enabled", models.BooleanField(default=False)),
                ("last_auth_on", models.DateTimeField(null=True)),
                ("external_id", models.CharField(max_length=128, null=True)),
                ("verification_token", models.CharField(max_length=64, null=True)),
                (
                    "email_status",
                    models.CharField(
                        choices=[
                            ("U", "Unverified"),
                            ("V", "Verified"),
                            ("F", "Failing"),
                        ],
                        default="U",
                        max_length=1,
                    ),
                ),
                (
                    "email_verification_secret",
                    models.CharField(db_index=True, max_length=64),
                ),
                (
                    "avatar",
                    models.ImageField(
                        null=True,
                        storage=storages.backends.s3.S3Storage(
                            bucket_name="temba-default",
                            default_acl="public-read",
                            querystring_auth=False,
                            signature_version="s3v4",
                        ),
                        upload_to=temba.utils.fields.UploadToIdPathAndRename("avatars/"),
                    ),
                ),
                ("is_system", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Invitation",
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
                ("email", models.EmailField(max_length=254)),
                ("secret", models.CharField(max_length=64, unique=True)),
                (
                    "role_code",
                    models.CharField(
                        choices=[
                            ("A", "Administrator"),
                            ("E", "Editor"),
                            ("T", "Agent"),
                        ],
                        default="E",
                        max_length=1,
                    ),
                ),
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
                "abstract": False,
            },
        ),
    ]
