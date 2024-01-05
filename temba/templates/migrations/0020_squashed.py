# Generated by Django 4.2.8 on 2024-01-05 15:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("orgs", "0133_squashed"),
        ("channels", "0181_squashed"),
    ]

    operations = [
        migrations.CreateModel(
            name="Template",
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
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                ("name", models.CharField(max_length=512)),
                (
                    "modified_on",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "org",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="templates",
                        to="orgs.org",
                    ),
                ),
            ],
            options={
                "unique_together": {("org", "name")},
            },
        ),
        migrations.CreateModel(
            name="TemplateTranslation",
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
                ("namespace", models.CharField(default="", max_length=36)),
                ("locale", models.CharField(max_length=6, null=True)),
                ("content", models.TextField(null=True)),
                ("components", models.JSONField(default=list)),
                ("params", models.JSONField(default=dict)),
                ("variable_count", models.IntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("A", "approved"),
                            ("P", "pending"),
                            ("R", "rejected"),
                            ("X", "unsupported_components"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
                ("external_id", models.CharField(max_length=64, null=True)),
                ("external_locale", models.CharField(max_length=6, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="template_translations",
                        to="channels.channel",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="translations",
                        to="templates.template",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["channel", "external_id"],
                        name="templatetranslations_by_ext",
                    )
                ],
            },
        ),
    ]
