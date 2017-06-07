from django.contrib.auth.models import User
from django.core import mail
from hc.test import BaseTestCase
from hc.api.models import Check


class LoginTestCase(BaseTestCase):

    def test_it_sends_link(self):
        initial_count = len(User.objects.all())
        check = Check()
        check.save()


        session = self.client.session
        session["welcome_code"] = str(check.code)
        session.save()
        form = {"email": "adrian@example.org"}
        response = self.client.post("/accounts/login/", form)
        assert response.status_code == 302

        # Assert that a user was created
        ##use count
        ##assert user exists
        user = User.objects.get(email=form["email"])
        final_count = len(User.objects.all())
        self.assertEqual(final_count, initial_count+1)

        # And email sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Log in to healthchecks.io')

        # Assert contents of the email body
        self.assertIn(self.profile.token, mail.outbox[0].body)

        # ## Assert that check is associated with the new user
    def test_check_is_associated_with_new_user(self):
        test_user = User.objects.get(email="alice@example.org")
        check = Check(user=self.alice)
        check.save()
        self.assertEqual(check.user.id, test_user.id)

    def test_it_pops_bad_link_from_session(self):
        self.client.session["bad_link"] = True
        self.client.get("/accounts/login/")
        assert "bad_link" not in self.client.session

        # ## Any other tests?
