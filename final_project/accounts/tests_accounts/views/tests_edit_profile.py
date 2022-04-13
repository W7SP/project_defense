from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from final_project.accounts.helpers import UserAndProfileData
from final_project.accounts.models import Profile

UserModel = get_user_model()


class EditProfileViewTests(UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'auth_accounts/edit_user.html'

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return user, profile

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('edit user', kwargs={'pk': profile.pk}))

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(profile)

        self.assertEqual(200, response.status_code)

    # CHECK IF VIEW DOESN'T LOAD WITHOUT A LOGGED-IN USER OR CORRECT USER ID
    def test_when_opening_without_logged_in_user_or_with_wrong_user__expect_302(self):
        response = self.client.get(reverse('edit user', kwargs={
            'pk': 1,
        }))

        self.assertEqual(302, response.status_code)

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(profile)

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF USER IS EDITED SUCCESSFULLY
    def test_edit_user_when_data_is_valid(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.client.post(
            reverse('edit user', kwargs={'pk': profile.pk}),
            data={
                'first_name': 'PetkoEdit',
                'last_name': 'Stankov',
                'picture': 'http://petko.com',
                'date_of_birth': date(2000, 4, 28),
                'gender': 'Male',
                'user': user,
            }
        )
        updated_profile = Profile.objects.get(pk=profile.pk)
        self.assertEqual('PetkoEdit', updated_profile.first_name)
