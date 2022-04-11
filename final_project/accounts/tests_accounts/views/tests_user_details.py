import logging
from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

from final_project.accounts.models import Profile

UserModel = get_user_model()


class ProfileDetailsViewTests(django_test.TestCase):
    EXPECTED_TEMPLATE = 'accounts_info/profile_details.html'

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

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        valid_user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=valid_user,
        )

        return valid_user, profile

    def test_view_renders_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.get(reverse_lazy('profile details', kwargs={'pk': profile.pk}))

        self.assertTemplateUsed(self.EXPECTED_TEMPLATE)

