from datetime import datetime, timezone as tzone

from django_redis import get_redis_connection

from temba.campaigns.models import Campaign, CampaignEvent
from temba.contacts.models import ContactField
from temba.tests import TembaTest
from temba.utils.uuid import uuid4


class CampaignEventTest(TembaTest):
    def test_get_recent_fires(self):
        contact1 = self.create_contact("Ann", phone="+1234567890")
        contact2 = self.create_contact("Bob", phone="+1234567891")
        farmers = self.create_group("Farmers", [contact1, contact2])
        campaign = Campaign.create(self.org, self.admin, "Reminders", farmers)
        planting_date = self.create_field("planting_date", "Planting Date", value_type=ContactField.TYPE_DATETIME)
        flow = self.create_flow("Test Flow")
        event1 = CampaignEvent.create_flow_event(
            self.org, self.admin, campaign, planting_date, offset=1, unit="W", flow=flow, delivery_hour=13
        )
        event2 = CampaignEvent.create_message_event(
            self.org, self.admin, campaign, planting_date, offset=3, unit="D", message="Hello", delivery_hour=9
        )

        def add_recent_contact(event, contact, ts: float):
            r = get_redis_connection()
            member = f"{uuid4()}|{contact.id}"
            r.zadd(f"recent_campaign_fires:{event.id}", mapping={member: ts})

        add_recent_contact(event1, contact1, 1639338554.969123)
        add_recent_contact(event1, contact2, 1639338555.234567)
        add_recent_contact(event2, contact1, 1639338561.345678)

        self.assertEqual(
            [
                {"contact": contact2, "time": datetime(2021, 12, 12, 19, 49, 15, 234567, tzone.utc)},
                {"contact": contact1, "time": datetime(2021, 12, 12, 19, 49, 14, 969123, tzone.utc)},
            ],
            event1.get_recent_fires(),
        )
        self.assertEqual(
            [
                {"contact": contact1, "time": datetime(2021, 12, 12, 19, 49, 21, 345678, tzone.utc)},
            ],
            event2.get_recent_fires(),
        )
