from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from final_project.accounts.models import Profile
from final_project.main.models import Courses

UserModel = get_user_model()


class CoursesTests(TestCase):
    # SET UP
    VALID_COACH_CREDENTIALS = {
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

    VALID_PARTICIPANT_CREDENTIALS = {
        'email': 'bogi@abv.bg',
        'password': '1234',
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

    def __create_profile(self, **information):
        profile = Profile(**information)
        profile = self.__add_user_to_profile(profile)
        return profile

    def __add_user_to_profile(self, profile):
        valid_user = self.__create_user(**self.VALID_PARTICIPANT_CREDENTIALS)
        profile.user = valid_user
        profile.save()
        return profile

    def __add_coach_and_participant_to_profile(self, course):
        valid_coach = self.__create_user(**self.VALID_COACH_CREDENTIALS)
        valid_participant = self.__create_profile(**self.VALID_PROFILE_DATA)
        course.coach = valid_coach
        course.participants.add(valid_participant)
        course.save()
        return course

    # CREATE COURSE SUCCESS
    def test_course_create__when_all_data_is_valid__expect_success(self):
        course = Courses.objects.create(**self.VALID_COURSE_DATA)
        course = self.__add_coach_and_participant_to_profile(course)

        self.assertIsNotNone(course.pk)
