# Generated by Django 4.0.4 on 2022-06-15 19:47
from collections import defaultdict

from django.db import migrations

ROLE_ADMINISTRATOR = "A"
ROLE_EDITOR = "E"
ROLE_VIEWER = "V"
ROLE_AGENT = "T"
ROLE_SURVEYOR = "S"


def backfill_org_membership(apps, schema_editor):
    Org = apps.get_model("orgs", "Org")

    role_counts = defaultdict(int)

    def add_user(o, u, r: str):
        o.users.add(u, through_defaults={"role_code": r})
        role_counts[r] += 1

    for org in Org.objects.all():
        for user in org.administrators.all():
            add_user(org, user, ROLE_ADMINISTRATOR)
        for user in org.editors.all():
            add_user(org, user, ROLE_EDITOR)
        for user in org.viewers.all():
            add_user(org, user, ROLE_VIEWER)
        for user in org.agents.all():
            add_user(org, user, ROLE_AGENT)
        for user in org.surveyors.all():
            add_user(org, user, ROLE_SURVEYOR)

    for role, count in role_counts.items():
        print(f"Added {count} users with role {role} to orgs")


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("orgs", "0098_orgmembership_org_users_orgmembership_org_and_more"),
    ]

    operations = [migrations.RunPython(backfill_org_membership, reverse)]
