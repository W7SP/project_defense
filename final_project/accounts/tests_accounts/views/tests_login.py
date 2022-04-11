from django import test as django_test
from django.urls import reverse


class LoginViewTests(django_test.TestCase):
    EXPECTED_TEMPLATE = 'auth_accounts/login.html'

    def test_view_renders_correct_template(self):
        response = self.client.get(reverse('login user'))

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)
