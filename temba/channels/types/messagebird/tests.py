from django.urls import reverse

from temba.tests import TembaTest

from ...models import Channel


class MessagebirdTypeTest(TembaTest):
    def setUp(self):
        super().setUp()

        self.channel = Channel.create(
            self.org,
            self.user,
            "US",
            "MBD",
            name="Messagebird: 12345",
            address="12345",
            role="SR",
            schemes=["tel"],
            config={
                "secret": "my_super_secret",
                "auth_token": "authtoken",
            },
        )

    def test_claim(self):
        url = reverse("channels.types.messagebird.claim")

        self.login(self.admin)

        # Switch to supported timezone
        self.org.timezone = "America/New_York"
        self.org.save()

        # beta- should not see the general channel claim page
        response = self.client.get(reverse("channels.channel_claim"))
        self.assertNotContains(response, url)

        self.make_beta(self.admin)

        # check that claim page URL appears on claim list page
        response = self.client.get(reverse("channels.channel_claim"))
        self.assertContains(response, url)
        # can fetch the claim page
        response = self.client.get(url)
        self.assertContains(response, "Connect Messagebird")

        post_data = response.context["form"].initial
        post_data["secret"] = "my_super_secret"
        post_data["auth_token"] = "authtoken"
        post_data["country"] = "US"
        post_data["number"] = "12345"

        response = self.client.post(url, post_data, follow=True)
        # assert our channel got created
        channel = Channel.objects.get(address="12345")
        self.assertEqual(channel.config[Channel.CONFIG_AUTH_TOKEN], "authtoken")
        self.assertEqual(
            channel.config[Channel.CONFIG_SECRET],
            "my_super_secret",
        )
        self.assertEqual(channel.address, "12345")
        self.assertEqual(channel.name, "Messagebird: 12345")
