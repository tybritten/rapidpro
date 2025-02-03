from datetime import datetime, timezone as tzone
from uuid import uuid4

from django.utils import timezone

from temba.contacts.models import ContactFire
from temba.flows.models import FlowSession
from temba.ivr.models import Call
from temba.tests import MigrationTest


class BackfillFiresTest(MigrationTest):
    app = "flows"
    migrate_from = "0364_flowsession_last_sprint_uuid"
    migrate_to = "0365_backfill_fires"

    def setUpBeforeMigration(self, apps):
        self.contact1 = self.create_contact("Ann", phone="+1234567890")
        self.contact2 = self.create_contact("Bob", phone="+1234567891")
        self.contact3 = self.create_contact("Cat", phone="+1234567892")
        self.call = Call.objects.create(
            org=self.org,
            channel=self.channel,
            direction=Call.DIRECTION_IN,
            contact=self.contact3,
            contact_urn=self.contact3.get_urn(),
            status="A",
            created_on=timezone.now(),
            duration=15,
        )

        self.session1 = FlowSession.objects.create(  # completed session
            uuid=uuid4(),
            org=self.org,
            contact=self.contact1,
            status="C",
            session_type="M",
            responded=False,
            output_url="http://session.json",
            ended_on=timezone.now(),
        )
        self.session2 = FlowSession.objects.create(  # waiting session with expiration
            uuid=uuid4(),
            org=self.org,
            contact=self.contact1,
            status="W",
            session_type="M",
            responded=False,
            output_url="http://session.json",
            wait_expires_on=datetime(2025, 1, 3, 15, 1, 30, 45, tzone.utc),
        )
        self.session3 = FlowSession.objects.create(  # waiting session with timeout
            uuid=uuid4(),
            org=self.org,
            contact=self.contact1,
            status="W",
            session_type="M",
            responded=False,
            output_url="http://session.json",
            timeout_on=datetime(2025, 1, 3, 15, 9, 30, 45, tzone.utc),
        )
        self.session4 = FlowSession.objects.create(  # both
            uuid=uuid4(),
            org=self.org,
            contact=self.contact2,
            status="W",
            session_type="M",
            responded=False,
            output_url="http://session.json",
            wait_expires_on=datetime(2025, 1, 3, 15, 24, 0, 0, tzone.utc),
            timeout_on=datetime(2025, 1, 3, 15, 25, 0, 0, tzone.utc),
        )
        self.session5 = FlowSession.objects.create(  # IVR session with expiration
            uuid=uuid4(),
            org=self.org,
            contact=self.contact3,
            status="W",
            session_type="V",
            call_id=self.call.id,
            responded=False,
            output_url="http://session.json",
            wait_expires_on=datetime(2025, 1, 3, 15, 26, 0, 0, tzone.utc),
        )

    def test_migration(self):
        self.session1.refresh_from_db()
        self.assertIsNone(self.session1.last_sprint_uuid)
        self.assertIsNone(self.session1.wait_expires_on)
        self.assertIsNone(self.session1.timeout_on)

        self.session2.refresh_from_db()
        self.assertIsNotNone(self.session2.last_sprint_uuid)
        self.assertIsNone(self.session2.wait_expires_on)
        self.assertIsNone(self.session2.timeout_on)

        self.session3.refresh_from_db()
        self.assertIsNotNone(self.session3.last_sprint_uuid)
        self.assertIsNone(self.session3.wait_expires_on)
        self.assertIsNone(self.session3.timeout_on)

        self.session4.refresh_from_db()
        self.assertIsNotNone(self.session4.last_sprint_uuid)
        self.assertIsNone(self.session4.wait_expires_on)
        self.assertIsNone(self.session4.timeout_on)

        self.session5.refresh_from_db()
        self.assertIsNotNone(self.session5.last_sprint_uuid)
        self.assertIsNone(self.session5.wait_expires_on)
        self.assertIsNone(self.session5.timeout_on)

        self.assertEqual(5, ContactFire.objects.count())
        self.assertTrue(
            ContactFire.objects.filter(
                contact=self.contact1,
                fire_type="E",
                scope="",
                fire_on=datetime(2025, 1, 3, 15, 1, 30, 45, tzone.utc),
                session_uuid=self.session2.uuid,
                sprint_uuid=self.session2.last_sprint_uuid,
            ).exists()
        )
        self.assertTrue(
            ContactFire.objects.filter(
                contact=self.contact1,
                fire_type="T",
                scope="",
                fire_on=datetime(2025, 1, 3, 15, 9, 30, 45, tzone.utc),
                session_uuid=self.session3.uuid,
                sprint_uuid=self.session3.last_sprint_uuid,
            ).exists()
        )
        self.assertTrue(
            ContactFire.objects.filter(
                contact=self.contact2,
                fire_type="E",
                scope="",
                fire_on=datetime(2025, 1, 3, 15, 24, 0, 0, tzone.utc),
                session_uuid=self.session4.uuid,
                sprint_uuid=self.session4.last_sprint_uuid,
            ).exists()
        )
        self.assertTrue(
            ContactFire.objects.filter(
                contact=self.contact2,
                fire_type="T",
                scope="",
                fire_on=datetime(2025, 1, 3, 15, 25, 0, 0, tzone.utc),
                session_uuid=self.session4.uuid,
                sprint_uuid=self.session4.last_sprint_uuid,
            ).exists()
        )
        self.assertTrue(
            ContactFire.objects.filter(
                contact=self.contact3,
                fire_type="E",
                scope="",
                fire_on=datetime(2025, 1, 3, 15, 26, 0, 0, tzone.utc),
                session_uuid=self.session5.uuid,
                sprint_uuid=self.session5.last_sprint_uuid,
            ).exists()
        )

        fire = ContactFire.objects.get(contact=self.contact3)
        self.assertEqual(
            {
                "call_id": self.call.id,
                "session_id": self.session5.id,
                "session_modified_on": self.session5.modified_on.isoformat(),
            },
            fire.extra,
        )
