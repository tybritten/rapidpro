# Generated by Django 5.1.4 on 2025-01-06 21:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("globals", "0013_squashed"),
        ("orgs", "0162_squashed"),
    ]

    operations = [
        migrations.AddField(
            model_name="global",
            name="org",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="globals",
                to="orgs.org",
            ),
        ),
    ]
