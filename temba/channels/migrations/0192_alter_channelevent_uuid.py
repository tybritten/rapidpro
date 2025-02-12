# Generated by Django 5.1.4 on 2025-02-12 17:14

from django.db import migrations, models

import temba.utils.uuid


class Migration(migrations.Migration):

    dependencies = [
        ("channels", "0191_remove_syncevent_created_by_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channelevent",
            name="uuid",
            field=models.UUIDField(default=temba.utils.uuid.uuid4, unique=True),
        ),
    ]
