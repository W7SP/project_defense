from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from final_project.accounts.helpers import UserAndProfileData
from final_project.accounts.models import Profile
from final_project.main.models import Courses

UserModel = get_user_model()


class ProfileCoursesViewTests(UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'accounts_info/user_courses.html'

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
        return self.client.get(reverse('user\'s courses'))

    def __add__coach_and_participants_to_course(self, user, profile):
        course = Courses.objects.create(**self.VALID_COURSE_DATA,
                                        coach=user)

        course.participants.add(profile)
        course.save()
        return course

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile()

        self.assertEqual(200, response.status_code)

    # CHECK IF VIEW DOESN'T LOAD WITHOUT A LOGGED-IN USER
    def test_when_opening_without_logged_in_user_or_with_wrong_user__expect_302(self):
        response = self.__get_response_for_profile()

        self.assertEqual(302, response.status_code)

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile()

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW SHOWS COURSES THE USER HAS BOUGHT
    def test_view_shows_courses_user_has_bought(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.__add__coach_and_participants_to_course(user, profile)

        response = self.__get_response_for_profile()
        current_participants = response.context['object_list'][0].participants

        self.assertEqual(profile, current_participants.first())
