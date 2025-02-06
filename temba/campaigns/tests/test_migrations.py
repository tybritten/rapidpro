from datetime import datetime, timezone as tzone

from django.utils import timezone

from temba.campaigns.models import Campaign, CampaignEvent, EventFire
from temba.contacts.models import ContactField, ContactFire
from temba.tests import MigrationTest


class ConvertEventFiresTest(MigrationTest):
    app = "campaigns"
    migrate_from = "0063_squashed"
    migrate_to = "0064_convert_eventfires"

    def setUpBeforeMigration(self, apps):
        self.contact1 = self.create_contact("Ann", phone="+1234567890")
        self.contact2 = self.create_contact("Bob", phone="+1234567891")
        farmers = self.create_group("Farmers", [self.contact1, self.contact2])
        campaign = Campaign.create(self.org, self.admin, "Reminders", farmers)
        planting_date = self.create_field("planting_date", "Planting Date", value_type=ContactField.TYPE_DATETIME)
        flow = self.create_flow("Test Flow")
        self.event1 = CampaignEvent.create_flow_event(
            self.org, self.admin, campaign, planting_date, offset=1, unit="W", flow=flow, delivery_hour=13
        )
        self.event2 = CampaignEvent.create_message_event(
            self.org, self.admin, campaign, planting_date, offset=3, unit="D", message="Hello", delivery_hour=9
        )

        EventFire.objects.create(
            event=self.event1, contact=self.contact1, scheduled=datetime(2025, 2, 1, 13, 0, 0, 0, tzone.utc)
        )
        EventFire.objects.create(
            event=self.event2, contact=self.contact1, scheduled=datetime(2025, 2, 2, 13, 0, 0, 0, tzone.utc)
        )
        EventFire.objects.create(
            event=self.event1, contact=self.contact2, scheduled=datetime(2025, 2, 3, 13, 0, 0, 0, tzone.utc)
        )
        EventFire.objects.create(
            event=self.event2,
            contact=self.contact2,
            scheduled=datetime(2025, 2, 4, 13, 0, 0, 0, tzone.utc),
            fired=timezone.now(),
        )

    def test_migration(self):
        self.assertEqual(0, EventFire.objects.filter(fired=None).count())
        self.assertEqual(1, EventFire.objects.exclude(fired=None).count())

        self.assertEqual(3, ContactFire.objects.count())

        fires = list(ContactFire.objects.order_by("contact_id", "scope"))
        self.assertEqual(self.org, fires[0].org)
        self.assertEqual(self.contact1, fires[0].contact)
        self.assertEqual(ContactFire.TYPE_CAMPAIGN, fires[0].fire_type)
        self.assertEqual(str(self.event1.id), fires[0].scope)
        self.assertEqual(datetime(2025, 2, 1, 13, 0, 0, 0, tzone.utc), fires[0].fire_on)
        self.assertEqual(self.org, fires[1].org)
        self.assertEqual(self.contact1, fires[1].contact)
        self.assertEqual(ContactFire.TYPE_CAMPAIGN, fires[1].fire_type)
        self.assertEqual(str(self.event2.id), fires[1].scope)
        self.assertEqual(datetime(2025, 2, 2, 13, 0, 0, 0, tzone.utc), fires[1].fire_on)
        self.assertEqual(self.org, fires[2].org)
        self.assertEqual(self.contact2, fires[2].contact)
        self.assertEqual(ContactFire.TYPE_CAMPAIGN, fires[2].fire_type)
        self.assertEqual(str(self.event1.id), fires[2].scope)
        self.assertEqual(datetime(2025, 2, 3, 13, 0, 0, 0, tzone.utc), fires[2].fire_on)
