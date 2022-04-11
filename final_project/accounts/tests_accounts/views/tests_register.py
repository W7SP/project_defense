from datetime import date

from django import test as django_test
from django.urls import reverse


class RegisterViewTests(django_test.TestCase):
    # SET UP
    EXPECTED_TEMPLATE = 'auth_accounts/register.html'

    VALID_USER_CREDENTIALS = {
        'email': 'petko.adm@abv.bg',
        'password': '123',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Petko',
        'last_name': 'Stankov',
        'picture': 'http://petko.com',
        'date_of_birth': date(2000, 4, 28),
        'gender': 'male',
        'account_balance': 100,
    }

    # CHECK IF REGISTER VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        response = self.client.get(reverse('register user'))

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF USER IS CREATED SUCCESSFULLY WHEN REGISTERED


