from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from final_project.accounts.helpers import UserAndProfileData
from final_project.accounts.models import Profile

UserModel = get_user_model()


class RegisterViewTests(django_test.TestCase):
    # SET UP
    EXPECTED_TEMPLATE = 'auth_accounts/register.html'

    VALID_REGISTER_DATA = {
        'email': 'petko.adm@abv.bg',
        'password': '123',
        'password_confirmation': 123,
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
    def test_view_registers_user_when_all_data_is_valid(self):
        self.client.post(
            reverse('register user'),
            data={
                'email': 'petko.adm@abv.bg',
                'password1': '#Petio2000',
                'password2': '#Petio2000',
                'first_name': 'Petko',
                'last_name': 'Stankov',
                'picture': 'http://petko.com',
                'date_of_birth': date(2000, 4, 28),
                'gender': 'Male',
                'account_balance': 100,
            },
        )

        profile = Profile.objects.first()
        user = UserModel.objects.first()
        expected_first_name = 'Petko'
        expected_email = 'petko.adm@abv.bg'
        expected_user_relation = user

        self.assertIsNotNone(user)
        self.assertIsNotNone(profile)
        self.assertEqual(expected_email, user.email)
        self.assertEqual(expected_first_name, profile.first_name)
        self.assertEqual(expected_user_relation, profile.user)



