from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        response = self.client.post(url, form)

        self.assertRedirects(response, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        query_channel_table = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(query_channel_table.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_{}/".format(frag)
            response = self.client.get(url)
            self.assertContains(response, "Integration Settings",
                                status_code=200)


class TeamAccessTestCase(BaseTestCase):
    # Test that the team access works
    def test_team_access_works(self):
        self.client.login(username="bob@example.org", password="password")

        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for kind_name in kinds:
            self.channel = Channel(user=self.alice, kind=kind_name)
            self.channel.value = "test that team access works"
            self.channel.save()

            url = "/integrations/{}/checks/".format(self.channel.code)

            self.response = self.client.get(url)
            self.assertEquals(self.response.status_code, 200)


# Test that bad kinds don't work//channels that raise Not implemented error
class BadKindTestCase(BaseTestCase):
    def test_bad_kind(self):
        self.client.login(username="alice@example.org", password="password")
        bad_kinds = ('0798885255', 'twitter', 'instagram', 'whatsapp',
                     'telegram', 'facebook', 'reddit')
        for any_kind in bad_kinds:
            url = "/integrations/add_{}/".format(any_kind)
            response = self.client.get(url)
            self.assertEquals(response.status_code, 404)
