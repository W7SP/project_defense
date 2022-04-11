from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from final_project.accounts.models import Profile
from final_project.main.models import Equipment

UserModel = get_user_model()


class EquipmentTests(TestCase):
    # SET UP
    VALID_SELLER_CREDENTIALS = {
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

    VALID_OWNER_CREDENTIALS = {
        'email': 'bogi@abv.bg',
        'password': '1234',
    }

    VALID_EQUIPMENT_DATA = {
        'name': 'WEIGHTS',
        'price': 100,
        'description': 'The best python web framework course',
        'picture': 'http://petko.com',
        'warranty': 4,
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_profile(self, **information):
        profile = Profile(**information)
        profile = self.__add_user_to_profile(profile)
        return profile

    def __add_user_to_profile(self, profile):
        valid_user = self.__create_user(**self.VALID_OWNER_CREDENTIALS)
        profile.user = valid_user
        profile.save()
        return profile

    def __add_seller_and_owner_to_profile(self, equipment):
        valid_seller = self.__create_user(**self.VALID_SELLER_CREDENTIALS)
        valid_owner = self.__create_profile(**self.VALID_PROFILE_DATA)
        equipment.seller = valid_seller
        equipment.owners.add(valid_owner)
        equipment.save()
        return equipment

    # CREATE COURSE SUCCESS
    def test_course_create__when_all_data_is_valid__expect_success(self):
        equipment = Equipment.objects.create(**self.VALID_EQUIPMENT_DATA)
        equipment = self.__add_seller_and_owner_to_profile(equipment)

        self.assertIsNotNone(equipment.pk)
