# Generated by Django 4.2.3 on 2023-10-23 18:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("triggers", "0035_backfill_trigger_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trigger",
            name="priority",
            field=models.IntegerField(),
        ),
    ]
