from final_project.main.models import Courses
from final_project.accounts.helpers import UserAndProfileData
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse
from final_project.accounts.models import Profile


UserModel = get_user_model()


class BuyCourseTests(UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'marketplace/buy_course.html'

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

        return (user, profile)

    def __get_response_for_profile(self, course):
        return self.client.get(reverse('buy course', kwargs={'pk': course.pk}))

    def __create_course_with_coach(self, user):
        course = Courses.objects.create(**self.VALID_COURSE_DATA, coach=user)
        return course

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        user, _ = self.__create_valid_user_and_profile()
        course = self.__create_course_with_coach(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(course)

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        user, _ = self.__create_valid_user_and_profile()
        course = self.__create_course_with_coach(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(course)

        self.assertEqual(200, response.status_code)

    # CHECK IF PROFILE CAN BUY BOOK WITH ENOUGH BUDGET CORRECTLY
    def test_user_can_buy_book_with_enough_budget__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        starting_budget = profile.account_balance
        course = self.__create_course_with_coach(user)
        expected_budget = starting_budget - course.price
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.client.post(
            reverse('buy course', kwargs={'pk': course.pk}),
            data={
                'participants': profile,
            }
        )

        bought_course = Courses.objects.get(participants=profile)
        participant = Profile.objects.get(pk=profile.pk)
        budget_after_buying_the_course = participant.account_balance
        expected_participant = profile

        self.assertEqual(expected_participant, bought_course.participants.first())
        self.assertEqual(expected_budget, budget_after_buying_the_course)

    # CHECK IF PROFILE CAN'T BUY BOOK WITHOUT ENOUGH BUDGET CORRECTLY
    def test_user_can_not_buy_book_without_enough_budget__expect_error_message(self):
        user, profile = self.__create_valid_user_and_profile()
        starting_budget = profile.account_balance
        course = self.__create_course_with_coach(user)
        course.price = 1000
        course.save()

        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(
            reverse('buy course', kwargs={'pk': course.pk}),
            data={
                'participants': profile,
            }
        )

        expected_participant = None
        actual_participant = course.participants.first()
        self.assertEqual(expected_participant, actual_participant)

        expected_error_message = b"You can't afford to buy this course!"
        self.assertEqual(expected_error_message, response.content)

        self.assertEqual(starting_budget, profile.account_balance)
