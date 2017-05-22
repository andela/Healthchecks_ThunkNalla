from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works
    def test_team_access(self):
        self.check = Check(user=self.alice)
        self.check.save()

        self.client.login(username="bob@example.org", password="password")

        url = "/checks/%s/timeout/" % self.check.code
        payload = {"timeout": 5000, "grace": 60}

        r = self.client.post(url, data=payload)
        self.assertRedirects(r, "/checks/")

        check = Check.objects.get(code=self.check.code)
        assert check.timeout.total_seconds() == 5000
        assert check.grace.total_seconds() == 60
