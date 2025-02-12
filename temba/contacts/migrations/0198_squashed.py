# Generated by Django 5.1.4 on 2025-01-06 21:25

import django.db.models.deletion
import django.db.models.functions.text
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("channels", "0188_squashed"),
        ("contacts", "0197_squashed"),
        ("orgs", "0162_squashed"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="org",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="contacts",
                to="orgs.org",
            ),
        ),
        migrations.AddField(
            model_name="contactfield",
            name="created_by",
            field=models.ForeignKey(
                help_text="The user which originally created this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_creations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactfield",
            name="modified_by",
            field=models.ForeignKey(
                help_text="The user which last modified this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_modifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactfield",
            name="org",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="fields",
                to="orgs.org",
            ),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="contacts",
            field=models.ManyToManyField(related_name="groups", to="contacts.contact"),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="created_by",
            field=models.ForeignKey(
                help_text="The user which originally created this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_creations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="modified_by",
            field=models.ForeignKey(
                help_text="The user which last modified this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_modifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="org",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="groups",
                to="orgs.org",
            ),
        ),
        migrations.AddField(
            model_name="contactgroup",
            name="query_fields",
            field=models.ManyToManyField(related_name="dependent_groups", to="contacts.contactfield"),
        ),
        migrations.AddField(
            model_name="contactgroupcount",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="counts",
                to="contacts.contactgroup",
            ),
        ),
        migrations.AddField(
            model_name="contactimport",
            name="created_by",
            field=models.ForeignKey(
                help_text="The user which originally created this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_creations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactimport",
            name="group",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="imports",
                to="contacts.contactgroup",
            ),
        ),
        migrations.AddField(
            model_name="contactimport",
            name="modified_by",
            field=models.ForeignKey(
                help_text="The user which last modified this item",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="%(app_label)s_%(class)s_modifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contactimport",
            name="org",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="contact_imports",
                to="orgs.org",
            ),
        ),
        migrations.AddField(
            model_name="contactimportbatch",
            name="contact_import",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="batches",
                to="contacts.contactimport",
            ),
        ),
        migrations.AddField(
            model_name="contactnote",
            name="contact",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="notes",
                to="contacts.contact",
            ),
        ),
        migrations.AddField(
            model_name="contactnote",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="contact_notes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="contacturn",
            name="channel",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="urns",
                to="channels.channel",
            ),
        ),
        migrations.AddField(
            model_name="contacturn",
            name="contact",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="urns",
                to="contacts.contact",
            ),
        ),
        migrations.AddField(
            model_name="contacturn",
            name="org",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="urns",
                to="orgs.org",
            ),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(
                condition=models.Q(("is_active", True)),
                fields=["org", "-modified_on", "-id"],
                name="contacts_by_org",
            ),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(
                condition=models.Q(("is_active", False)),
                fields=["org", "-modified_on", "-id"],
                name="contacts_by_org_deleted",
            ),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(fields=["org", "-modified_on"], name="contacts_contact_org_modified"),
        ),
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(fields=["modified_on"], name="contacts_modified"),
        ),
        migrations.AddConstraint(
            model_name="contact",
            constraint=models.CheckConstraint(
                condition=models.Q(("status__in", ("A", "B", "S", "V"))),
                name="contact_status_valid",
            ),
        ),
        migrations.AddConstraint(
            model_name="contactgroup",
            constraint=models.UniqueConstraint(
                models.F("org"),
                django.db.models.functions.text.Lower("name"),
                name="unique_contact_group_names",
            ),
        ),
        migrations.AddIndex(
            model_name="contactgroupcount",
            index=models.Index(
                condition=models.Q(("is_squashed", False)),
                fields=["group"],
                name="contactgroupcounts_unsquashed",
            ),
        ),
        migrations.AddConstraint(
            model_name="contacturn",
            constraint=models.CheckConstraint(
                condition=models.Q(("scheme", ""), ("path", ""), _connector="OR", _negated=True),
                name="non_empty_scheme_and_path",
            ),
        ),
        migrations.AddConstraint(
            model_name="contacturn",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    (
                        "identity",
                        django.db.models.functions.text.Concat(models.F("scheme"), models.Value(":"), models.F("path")),
                    )
                ),
                name="identity_matches_scheme_and_path",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="contacturn",
            unique_together={("identity", "org")},
        ),
    ]
