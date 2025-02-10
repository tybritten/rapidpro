# Generated by Django 5.1.4 on 2025-02-10 20:56

from django.db import migrations

SQL = """
DROP TRIGGER temba_flowrun_on_delete ON flows_flowrun;
DROP FUNCTION temba_flowrun_on_delete();
"""


class Migration(migrations.Migration):

    dependencies = [
        ("flows", "0368_remove_flowsession_modified_on_and_more"),
    ]

    operations = [migrations.RunSQL(SQL)]
