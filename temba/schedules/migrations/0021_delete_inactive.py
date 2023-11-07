# Generated by Django 4.2.3 on 2023-11-07 16:24

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def delete_inactive_schedules(apps, schema_editor):
    Broadcast = apps.get_model("msgs", "Broadcast")
    Schedule = apps.get_model("schedules", "Schedule")
    Trigger = apps.get_model("triggers", "Trigger")

    num_deleted = 0

    while True:
        id_batch = list(Schedule.objects.filter(is_active=False).values_list("id", flat=True)[:1000])
        if not id_batch:
            break

        Broadcast.objects.filter(schedule_id__in=id_batch).update(schedule=None)
        Trigger.objects.filter(schedule_id__in=id_batch).update(schedule=None)

        del_count, _ = Schedule.objects.filter(id__in=id_batch).delete()
        num_deleted += del_count

    if num_deleted:
        print(f"Deleted {num_deleted} inactive schedules")


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("schedules", "0020_delete_ended"),
    ]

    operations = [
        migrations.RunPython(delete_inactive_schedules, reverse),
        migrations.AlterField(
            model_name="schedule",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="schedules_schedule_creations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="modified_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="schedules_schedule_modifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="modified_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
