# Generated by Django 5.1.4 on 2025-02-25 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flows", "0377_remove_flowsession_flowsessions_contact_waiting"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flowrun",
            name="session",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="flows.flowsession"),
        ),
        migrations.AlterField(
            model_name="flowsession",
            name="status",
            field=models.CharField(
                choices=[("W", "Waiting"), ("C", "Completed"), ("I", "Interrupted"), ("X", "Expired"), ("F", "Failed")],
                max_length=1,
            ),
        ),
    ]
