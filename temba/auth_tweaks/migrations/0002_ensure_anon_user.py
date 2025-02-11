# Generated by Django 1.11.6 on 2018-07-16 20:43

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import migrations


def ensure_anon_user_exists(apps, schema_editor):
    User = get_user_model()

    if not User.objects.filter(username=settings.ANONYMOUS_USER_NAME).exists():  # pragma: no cover
        user = User(username=settings.ANONYMOUS_USER_NAME)
        user.set_unusable_password()
        user.save()


class Migration(migrations.Migration):
    dependencies = [("auth_tweaks", "0001_initial"), ("orgs", "0163_squashed")]

    operations = [migrations.RunPython(ensure_anon_user_exists)]
