from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddPushoverTestCase(BaseTestCase):
    def test_it_adds_channel(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=n&prio=0"
        response = self.client.get("/integrations/add_pushover/?{}".
                                   format(params))
        self.assertEquals(response.status_code, 302)

        channels = list(Channel.objects.all())
        self.assertEquals(len(channels), 1)
        self.assertEquals(channels[0].value, "a|0")

    @override_settings(PUSHOVER_API_TOKEN=None)
    def test_it_requires_api_token(self):
        self.client.login(username="alice@example.org", password="password")

        response = self.client.get("/integrations/add_pushover/")
        self.assertEqual(response.status_code, 404)

    def test_it_validates_nonce(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=INVALID&prio=0"
        response = self.client.get("/integrations/add_pushover/?{}".
                                   format(params))
        self.assertEquals(response.status_code, 403)

    # Test that pushover validates priority
    def test_reject_wrong_priority(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        priority_list = ['9', '-9', 'a', '#', 9, -9]
        for each_priority in priority_list:
            params = "pushover_user_key=a&nonce=n&prio={}".\
                format(each_priority)
            response = self.client.get("/integrations/add_pushover/?{}"
                                       .format(params))
            self.assertEquals(response.status_code, 400)

    def test_priority_works_negative(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        priority = '-1'

        params = "pushover_user_key=a&nonce=n&prio={}".format(priority)
        response = self.client.get("/integrations/add_pushover/?{}"
                                   .format(params))
        self.assertEquals(response.status_code, 302)

    def test_priority_works_positive(self):
        self.client.login(username="bob@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        priority = '2'

        params = "pushover_user_key=a&nonce=n&prio={}".format(priority)
        response = self.client.get("/integrations/add_pushover/?{}"
                                   .format(params))

        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/integrations/')

    def test_priority_works_zero(self):
        self.client.login(username="charlie@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        priority = '0'

        params = "pushover_user_key=a&nonce=n&prio={}".format(priority)
        response = self.client.get("/integrations/add_pushover/?{}"
                                   .format(params))
        self.assertRedirects(response, '/integrations/')
