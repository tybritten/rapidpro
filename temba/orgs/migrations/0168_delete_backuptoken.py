# Generated by Django 5.1.4 on 2025-02-11 21:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orgs", "0167_alter_backuptoken_user"),
        ("users", "0004_copy_backup_token"),
    ]

    operations = [
        migrations.DeleteModel(name="BackupToken"),
    ]
