from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from final_project.accounts.helpers import UserAndProfileData
from final_project.accounts.models import Profile
from final_project.main.models import StudyBook
from final_project.main.tests_main.views.tests_books import ValidStudyBookData

UserModel = get_user_model()


class BookShopTests(ValidStudyBookData, UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'marketplace/books_shop.html'

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_studybook_view(self):
        return StudyBook.objects.create(**self.VALID_STUDYBOOK_DATA)

    def __get_response_for_profile(self):
        return self.client.get(reverse('book shop'))

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

    # CHECK IF VIEW SHOWS ALL STUDYBOOK OBJECTS IN THE SHOP
    def test_view_shows_all_books_in_shop(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        first_book = self.__create_studybook_view()
        second_book = self.__create_studybook_view()
        thrird_book = self.__create_studybook_view()

        response = self.__get_response_for_profile()

        expected_books_count = 3
        actual_books_count = len(response.context['object_list'])

        self.assertEqual(expected_books_count, actual_books_count)


