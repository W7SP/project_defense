from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy

from final_project.accounts.models import Profile
from final_project.main.models import StudyBook, Equipment

UserModel = get_user_model()


class ProfileProductsViewTests(django_test.TestCase):
    # SET UP
    EXPECTED_TEMPLATE = 'accounts_info/user_products.html'

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

    VALID_STUDYBOOK_DATA = {
        'name': 'Atomic Habits',
        'price': 10,
        'cover': 'http://petko.com',
        'description': 'cool book description',
        'link_to_online_book': 'http://petko.com',
    }

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

    def __get_response_for_profile(self):
        return self.client.get(reverse('user\'s products'))

    def __add__author_and_owners_to_studybook(self, user, profile):
        studybook = StudyBook.objects.create(**self.VALID_STUDYBOOK_DATA,
                                             author=user)

        studybook.owners.add(profile)
        studybook.save()
        return studybook

    def __add__seller_and_owners_to_equipment(self, user, profile):
        equipment = Equipment.objects.create(**self.VALID_EQUIPMENT_DATA,
                                             seller=user)

        equipment.owners.add(profile)
        equipment.save()
        return equipment

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        response = self.__get_response_for_profile()

        self.assertTemplateUsed(self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile()
        self.assertEqual(200, response.status_code)

    # CHECK IF VIEW DOESN'T LOAD WITHOUT A LOGGED-IN USER OR CORRECT USER ID
    def test_when_opening_without_logged_in_user_or_with_wrong_user__expect_302(self):
        response = self.__get_response_for_profile()

        self.assertEqual(302, response.status_code)

    # CHECK IF VIEW SHOWS BOOKS THAT THE USER HAS BOUGHT
    def test_view_shows_studybooks_user_has_bought(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.__add__author_and_owners_to_studybook(user, profile)

        response = self.__get_response_for_profile()
        current_owners = response.context['books'][0].owners

        self.assertEqual(profile, current_owners.first())

    # CHECK IF VIEW SHOWS EQUIPMENT THAT THE USER HAS BOUGHT
    def test_view_shows_equipment_user_has_bought(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.__add__seller_and_owners_to_equipment(user, profile)

        response = self.__get_response_for_profile()
        current_owners = response.context['equipments'][0].owners

        self.assertEqual(profile, current_owners.first())
