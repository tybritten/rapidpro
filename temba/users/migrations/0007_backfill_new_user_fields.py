# Generated by Django 5.1.4 on 2025-02-12 15:29

from django.db import migrations


def copy_settings(apps, schema_editor):
    UserSettings = apps.get_model("orgs", "UserSettings")

    num_updated = 0
    for settings in UserSettings.objects.all().select_related("user"):
        settings.user.language = settings.language
        settings.user.last_auth_on = settings.last_auth_on
        settings.user.avatar = settings.avatar
        settings.user.is_system = settings.is_system
        settings.user.two_factor_enabled = settings.two_factor_enabled
        settings.user.two_factor_secret = settings.otp_secret
        settings.user.email_status = settings.email_status
        settings.user.email_verification_secret = settings.email_verification_secret
        settings.user.external_id = settings.external_id
        settings.user.verification_token = settings.verification_token
        settings.user.save(
            update_fields=(
                "language",
                "last_auth_on",
                "avatar",
                "is_system",
                "two_factor_enabled",
                "two_factor_secret",
                "email_status",
                "email_verification_secret",
                "external_id",
                "verification_token",
            )
        )
        num_updated += 1

    if num_updated:
        print(f"Updated {num_updated} users")


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_add_new_user_fields"),
    ]

    operations = [
        migrations.RunPython(copy_settings, migrations.RunPython.noop),
    ]
