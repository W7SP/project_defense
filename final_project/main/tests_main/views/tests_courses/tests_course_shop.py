from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from final_project.accounts.helpers import UserAndProfileData
from final_project.accounts.models import Profile
from final_project.main.models import Courses
from final_project.main.tests_main.views.tests_courses.init import ValidCourseData

UserModel = get_user_model()


class CourseShopTests(ValidCourseData, UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'marketplace/courses_shop.html'

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __create_course_view(self):
        return Courses.objects.create(**self.VALID_COURSE_DATA)

    def __get_response_for_profile(self):
        return self.client.get(reverse('courses shop'))

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
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
    def test_view_shows_all_books_in_shop(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        first_course = self.__create_course_view()
        second_course = self.__create_course_view()
        third_course = self.__create_course_view()
        print(first_course, second_course, third_course)

        response = self.__get_response_for_profile()

        expected_course_count = 3
        actual_course_count = len(response.context['object_list'])

        self.assertEqual(expected_course_count, actual_course_count)
