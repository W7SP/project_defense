from datetime import date

from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse

from final_project.accounts.models import Profile
from final_project.main.models import Courses

UserModel = get_user_model()


class ProfileCoursesViewTests(django_test.TestCase):
    EXPECTED_TEMPLATE = 'accounts_info/user_courses.html'

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
        valid_user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=valid_user,
        )

        return valid_user, profile

    def __add__participants_to_course(self, course, profile):
        course.participants.add(profile)
        course.save()
        return course

    def __get_response_for_profile(self):
        return self.client.get(reverse('user\'s courses'))

    # CHECK IF VIEW SHOWS COURSES THE USER HAS BOUGHT
    def test_view_shows_courses_user_has_bought(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA,
                                         user=user)
        course = Courses.objects.create(**self.VALID_COURSE_DATA,
                                        coach=user)

        course.participants.add(profile)
        course.save()

        response = self.__get_response_for_profile()
        check = response.context
        print(check)

        self.assertEqual(profile, course.participants.first())



    # def test_view_renders_correct_template(self):
    #     response = self.client.get('/accounts/user/courses/')
    #     print(response['location'])
    #     print(response)
    #     self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)
