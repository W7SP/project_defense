from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from final_project.accounts.models import Profile
from final_project.main.models import Equipment, StudyBook

UserModel = get_user_model()


class StudyBookTests(TestCase):
    # SET UP
    VALID_AUTHOR_CREDENTIALS = {
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

    VALID_STUDYBOOK_DATA = {
        'name': 'Atomic Habits',
        'price': 100,
        'description': 'The best book for improving your habits',
        'cover': 'http://petko.com',
        'link_to_online_book': 'http://petko.com',
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

    def __add_seller_and_owner_to_profile(self, studybook):
        valid_author = self.__create_user(**self.VALID_AUTHOR_CREDENTIALS)
        valid_owner = self.__create_profile(**self.VALID_PROFILE_DATA)
        studybook.author = valid_author
        studybook.owners.add(valid_owner)
        studybook.save()
        return studybook

    # CREATE COURSE SUCCESS
    def test_course_create__when_all_data_is_valid__expect_success(self):
        studybook = StudyBook.objects.create(**self.VALID_STUDYBOOK_DATA)
        studybook = self.__add_seller_and_owner_to_profile(studybook)

        self.assertIsNotNone(studybook.pk)
