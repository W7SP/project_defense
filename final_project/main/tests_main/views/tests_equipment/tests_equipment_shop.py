from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from final_project.accounts.helpers import UserAndProfileData
from final_project.accounts.models import Profile
from final_project.main.models import Equipment

UserModel = get_user_model()


class EquipmentShopTests(UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'marketplace/equipment_shop.html'

    VALID_EQUIPMENT_DATA = {
        'name': 'yoga math',
        'picture': 'http://petko.com',
        'price': 10,
        'description': 'epic yoga amth best buy',
        'warranty': 2,
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_equipment_view(self):
        return Equipment.objects.create(**self.VALID_EQUIPMENT_DATA)

    def __get_response_for_profile(self):
        return self.client.get(reverse('equipment shop'))

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile()

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile()

        self.assertEqual(200, response.status_code)

    # CHECK IF VIEW SHOWS ALL COURSES OBJECTS IN THE SHOP
    def test_view_shows_all_equipment_in_shop(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        first_equipment = self.__create_equipment_view()
        second_equipment = self.__create_equipment_view()
        third_equipment = self.__create_equipment_view()
        print(first_equipment, second_equipment, third_equipment)

        response = self.__get_response_for_profile()

        expected_equipment_count = 3
        actual_equipment_count = len(response.context['object_list'])

        self.assertEqual(expected_equipment_count, actual_equipment_count)
