# Generated by Django 4.2.8 on 2024-01-05 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("orgs", "0133_squashed"),
        ("airtime", "0026_squashed"),
    ]

    operations = [
        migrations.AddField(
            model_name="airtimetransfer",
            name="org",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="airtime_transfers",
                to="orgs.org",
            ),
        ),
    ]
