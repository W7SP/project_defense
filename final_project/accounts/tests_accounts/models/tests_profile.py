from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

from final_project.accounts.models import Profile

UserModel = get_user_model()


class ProfileTests(TestCase):
    # SET UP
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

    VALID_PROFILE_DATA_TEST_FIRST_NAME = {
        'last_name': 'Stankov',
        'picture': 'http://petko.com',
        'date_of_birth': date(2000, 4, 28),
        'gender': 'male',
        'account_balance': 100,
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __add_user_to_profile(self, profile):
        valid_user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile.user = valid_user
        profile.save()
        return profile

    # CREATE PROFILE SUCCESS
    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        profile = self.__add_user_to_profile(profile)

        self.assertIsNotNone(profile.pk)

    # TESTS FIRST NAME CHARACTER VALIDATION
    def test_profile_create__when_first_name_contains_a_digit__expect_to_fail(self):
        first_name = '5ko'
        profile = Profile(first_name, **self.VALID_PROFILE_DATA_TEST_FIRST_NAME)
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_dollar_sign__expect_to_fail(self):
        first_name = 'Petko$'
        profile = Profile(first_name, **self.VALID_PROFILE_DATA_TEST_FIRST_NAME)
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_to_fail(self):
        first_name = 'Pet ko'
        profile = Profile(first_name, **self.VALID_PROFILE_DATA_TEST_FIRST_NAME)
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_underscore__expect_to_fail(self):
        first_name = 'Pet_ko'
        profile = Profile(first_name, **self.VALID_PROFILE_DATA_TEST_FIRST_NAME)
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    # TESTS FIRST NAME CHARACTER VALIDATION
    def test_profile_create__when_first_name_is_too_short__expect_to_fail(self):
        first_name = 'Petk'
        profile = Profile(first_name, **self.VALID_PROFILE_DATA_TEST_FIRST_NAME)
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    # TESTS LAST NAME CHARACTER VALIDATION
    def test_profile_create__when_last_name_contains_a_digit__expect_to_fail(self):
        last_name = 'Stankov5'
        profile = Profile(
            first_name=self.VALID_PROFILE_DATA['first_name'],
            last_name=last_name,
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            gender=self.VALID_PROFILE_DATA['gender'],
            account_balance=self.VALID_PROFILE_DATA['account_balance'],
        )
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_contains_a_dollar_sign__expect_to_fail(self):
        last_name = 'Stankov$'
        profile = Profile(
            first_name=self.VALID_PROFILE_DATA['first_name'],
            last_name=last_name,
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            gender=self.VALID_PROFILE_DATA['gender'],
            account_balance=self.VALID_PROFILE_DATA['account_balance'],
        )
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_contains_a_space__expect_to_fail(self):
        last_name = 'Stan kov'
        profile = Profile(
            first_name=self.VALID_PROFILE_DATA['first_name'],
            last_name=last_name,
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            gender=self.VALID_PROFILE_DATA['gender'],
            account_balance=self.VALID_PROFILE_DATA['account_balance'],
        )
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_last_name_contains_a_underscore__expect_to_fail(self):
        last_name = 'Stan_kov'
        profile = Profile(
            first_name=self.VALID_PROFILE_DATA['first_name'],
            last_name=last_name,
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            gender=self.VALID_PROFILE_DATA['gender'],
            account_balance=self.VALID_PROFILE_DATA['account_balance'],
        )
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    # TESTS LAST NAME CHARACTER VALIDATION
    def test_profile_create__when_last_name_is_too_short__expect_to_fail(self):
        last_name = 'Stan'
        profile = Profile(
            first_name=self.VALID_PROFILE_DATA['first_name'],
            last_name=last_name,
            picture=self.VALID_PROFILE_DATA['picture'],
            date_of_birth=self.VALID_PROFILE_DATA['date_of_birth'],
            gender=self.VALID_PROFILE_DATA['gender'],
            account_balance=self.VALID_PROFILE_DATA['account_balance'],
        )
        profile = self.__add_user_to_profile(profile)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()  # This is called in ModelForms implicitly
            profile.save()

        self.assertIsNotNone(context.exception)

    # TEST PROPERTY FULL NAME
    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(**self.VALID_PROFILE_DATA)
        profile = self.__add_user_to_profile(profile)

        expected_fullname = f'{self.VALID_PROFILE_DATA["first_name"]} {self.VALID_PROFILE_DATA["last_name"]}'
        self.assertEqual(expected_fullname, profile.full_name)
        self.assertEqual(expected_fullname, str(profile))

    # def test_profile_create__when_first_name_is_too_long__expect_to_fail(self):
    #     first_name = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    #     profile = Profile(first_name, **self.VALID_PROFILE_DATA_TEST_FIRST_NAME)
    #     profile = self.__add_user_to_profile(profile)
    #
    #     with self.assertRaises(Error) as context:
    #         profile.full_clean()  # This is called in ModelForms implicitly
    #         profile.save()
    #
    #     self.assertIsNotNone(context.exception)



