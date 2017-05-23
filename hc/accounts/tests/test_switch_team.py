from hc.test import BaseTestCase
from hc.api.models import Check


class SwitchTeamTestCase(BaseTestCase):

    def test_it_switches(self):
        check_test = Check(user=self.alice, name="This belongs to Alice")
        check_test.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/accounts/switch_team/%s/" % self.alice.username
        response= self.client.get(url, follow=True)
        # Assert the contents of response
        self.assertIn(str.encode("<title>My Checks - healthchecks.io</title>\n"), response.content)

    def test_it_checks_team_membership(self):
        self.client.login(username="charlie@example.org", password="password")

        url = "/accounts/switch_team/{}/".format(self.alice.username)
        response = self.client.get(url)
        # Assert the expected error code
        self.assertEqual(response.status_code, 403)

    def test_it_switches_to_own_team(self):
        self.client.login(username="alice@example.org", password="password")
        url = "/accounts/switch_team/{}/" .format(self.alice.username)
        response = self.client.get(url, follow=True)
        # Assert the expected error code
        self.assertEqual(response.status_code, 200)
