from datetime import date
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse
from final_project.accounts.models import Profile
from final_project.main.models import Courses, StudyBook, Equipment

UserModel = get_user_model()


class ProfileProductsViewTests(django_test.TestCase):
    # SET UP USER AND PROFILE
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

    # SET UP PRODUCT
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

    VALID_COURSE_DATA = {
        'name': 'Python_Web',
        'price': 100,
        'description': 'The best python web framework course',
        'picture': 'http://petko.com',
        'duration': 4,
        'link_to_platform': 'https://youtu.be/iqLlvbaH30g',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return user, profile

    def __get_response_for_profile(self):
        return self.client.get(reverse('user\'s listings'))

    def __add__seller_to_product(self, listing, user):
        if listing == 'StudyBook':
            product = StudyBook.objects.create(**self.VALID_STUDYBOOK_DATA, author=user)

        elif listing == 'Courses':
            product = Courses.objects.create(**self.VALID_COURSE_DATA, coach=user)

        else:
            product = Equipment.objects.create(**self.VALID_EQUIPMENT_DATA, seller=user)

        product.save()
        return product

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile()

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

    # CHECK IF VIEW SHOWS BOOKS THAT THE USER HAS LISTED ON THE MARKET
    def test_view_shows_studybooks_user_has_listed_for_sale(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.__add__seller_to_product('StudyBook', user)

        response = self.__get_response_for_profile()
        current_seller = response.context['books'][0].author

        self.assertEqual(user, current_seller)

    # CHECK IF VIEW SHOWS EQUIPMENT THAT THE USER HAS LISTED ON THE MARKET
    def test_view_shows_equipment_user_has_listed_for_sale(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.__add__seller_to_product('Equipment', user)

        response = self.__get_response_for_profile()
        current_seller = response.context['equipments'][0].seller

        self.assertEqual(user, current_seller)

    # CHECK IF VIEW SHOWS COURSES THAT THE USER HAS LISTED ON THE MARKET
    def test_view_shows_courses_user_has_listed_for_sale(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.__add__seller_to_product('Courses', user)

        response = self.__get_response_for_profile()
        current_seller = response.context['courses'][0].coach

        self.assertEqual(user, current_seller)
