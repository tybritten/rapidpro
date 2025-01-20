from datetime import datetime, timezone as tzone

from temba.flows.models import FlowSession
from temba.tests import MigrationTest
from temba.utils.uuid import uuid4


class BackfillSessionModifiedOn(MigrationTest):
    app = "flows"
    migrate_from = "0358_flowsession_modified_on"
    migrate_to = "0359_backfill_session_modified_on"

    def setUpBeforeMigration(self, apps):
        contact = self.create_contact("Bob", phone="+1234567890")
        flow = self.create_flow("Test")

        self.session1 = FlowSession.objects.create(
            uuid=uuid4(),
            org=self.org,
            contact=contact,
            current_flow=flow,
            status=FlowSession.STATUS_WAITING,
            output_url="http://sessions.com/123.json",
            created_on=datetime(2025, 1, 1, 0, 0, 0, 0, tzone.utc),
            wait_started_on=datetime(2025, 1, 2, 0, 0, 0, 0, tzone.utc),
            wait_expires_on=datetime(2025, 1, 3, 0, 0, 0, 0, tzone.utc),
            wait_resume_on_expire=False,
        )
        self.session2 = FlowSession.objects.create(
            uuid=uuid4(),
            org=self.org,
            contact=contact,
            current_flow=flow,
            status=FlowSession.STATUS_COMPLETED,
            output_url="http://sessions.com/123.json",
            created_on=datetime(2025, 1, 1, 0, 0, 0, 0, tzone.utc),
            ended_on=datetime(2025, 1, 4, 0, 0, 0, 0, tzone.utc),
            wait_started_on=None,
            wait_expires_on=None,
            wait_resume_on_expire=False,
        )
        self.session3 = FlowSession.objects.create(
            uuid=uuid4(),
            org=self.org,
            contact=contact,
            current_flow=flow,
            status=FlowSession.STATUS_COMPLETED,
            output_url="http://sessions.com/123.json",
            created_on=datetime(2025, 1, 1, 0, 0, 0, 0, tzone.utc),
            modified_on=datetime(2025, 1, 3, 12, 0, 0, 0, tzone.utc),
            ended_on=datetime(2025, 1, 4, 0, 0, 0, 0, tzone.utc),
            wait_started_on=None,
            wait_expires_on=None,
            wait_resume_on_expire=False,
        )

    def test_migration(self):
        def assert_modified_on(session, expected):
            session.refresh_from_db()
            self.assertEqual(session.modified_on, expected)

        assert_modified_on(self.session1, datetime(2025, 1, 3, 0, 0, 0, 0, tzone.utc))
        assert_modified_on(self.session2, datetime(2025, 1, 4, 0, 0, 0, 0, tzone.utc))
        assert_modified_on(self.session3, datetime(2025, 1, 3, 12, 0, 0, 0, tzone.utc))  # unchanged
