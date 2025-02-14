from django.utils import timezone

from temba.flows.models import FlowSession
from temba.tests import MigrationTest


class BackfillCurrentSessionUUIDTest(MigrationTest):
    app = "contacts"
    migrate_from = "0201_contact_current_session_uuid"
    migrate_to = "0202_backfill_current_session_uuid"

    def setUpBeforeMigration(self, apps):
        self.flow = self.create_flow("Test 1")

        def create_contact(name, phone, flow):
            contact = self.create_contact(name, phone=phone)
            contact.current_flow = flow
            contact.save(update_fields=("current_flow",))
            return contact

        def create_waiting_session(contact, uuid):
            return FlowSession.objects.create(
                uuid=uuid,
                org=self.org,
                contact=contact,
                status=FlowSession.STATUS_WAITING,
                output_url="http://sessions.com/123.json",
                created_on=timezone.now(),
            )

        # contacts 1 & 2: has flow set, has waiting session
        self.contact1 = create_contact("Ann", "+1234567801", self.flow)
        create_waiting_session(self.contact1, "9989032c-56b1-42ec-9e81-2512c42a6e9e")
        self.contact2 = create_contact("Bob", "+1234567802", self.flow)
        create_waiting_session(self.contact2, "c74adad1-f3c1-4c3d-9b08-2da06a5958de")

        # contact 3: has flow set, has no waiting session
        self.contact3 = create_contact("Cat", "+1234567803", self.flow)

        # contact 4: has flow set, has two waiting sessions
        self.contact4 = create_contact("Dan", "+1234567804", self.flow)
        create_waiting_session(self.contact4, "f6efb64a-d92f-458b-b140-f1d75cd277a2")
        create_waiting_session(self.contact4, "f5f83e58-a9f6-416b-bdb7-001c9a8f624c")

        # contact 5: no flow set, no waiting session
        self.contact5 = create_contact("Eve", "+1234567805", None)

    def test_migration(self):
        def assert_current_session(contact, session_uuid, flow):
            contact.refresh_from_db()
            self.assertEqual(session_uuid, str(contact.current_session_uuid) if contact.current_session_uuid else None)
            self.assertEqual(flow, contact.current_flow)

        assert_current_session(self.contact1, "9989032c-56b1-42ec-9e81-2512c42a6e9e", self.flow)
        assert_current_session(self.contact2, "c74adad1-f3c1-4c3d-9b08-2da06a5958de", self.flow)
        assert_current_session(self.contact3, None, None)  # current_flow cleared
        assert_current_session(self.contact4, "f5f83e58-a9f6-416b-bdb7-001c9a8f624c", self.flow)
        assert_current_session(self.contact5, None, None)  # unchanged
