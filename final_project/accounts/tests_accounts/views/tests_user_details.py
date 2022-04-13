import logging
from datetime import date
from django.contrib.auth.models import Group

from django import test as django_test
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from final_project.accounts.helpers import UserAndProfileData
from final_project.accounts.models import Profile

UserModel = get_user_model()


class ProfileDetailsViewTests(UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'accounts_info/profile_details.html'

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))

    def __create_group_and_add_user(self, user, group_name):
        group = Group.objects.get_or_create(name=group_name)
        user.groups.add(group[0])
        user.save()
        return group

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        login_result = self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(profile)

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(profile)

        self.assertEqual(200, response.status_code)

    # CHECK IF VIEW DOESN'T LOAD WITHOUT A LOGGED-IN USER OR CORRECT USER ID
    def test_when_opening_without_logged_in_user_or_with_wrong_user__expect_302(self):
        response = self.client.get(reverse('profile details', kwargs={
            'pk': 1,
        }))

        self.assertEqual(302, response.status_code)

    # CHECK IF USER HAS CORRECT JOB TEST: (TRAINER)
    def test_logged_in_user_has_correct_job_expect_trainer(self):
        user, profile = self.__create_valid_user_and_profile()
        self.__create_group_and_add_user(user, 'Trainers')
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))

        expected_job = 'Trainer'
        actual_job = response.context['job']
        self.assertEqual(expected_job, actual_job)

    # CHECK IF USER HAS CORRECT JOB TEST: (AUTHOR)
    def test_logged_in_user_has_correct_job_expect_author(self):
        user, profile = self.__create_valid_user_and_profile()
        self.__create_group_and_add_user(user, 'Authors')
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))

        expected_job = 'Author'
        actual_job = response.context['job']
        self.assertEqual(expected_job, actual_job)

    # CHECK IF USER HAS CORRECT JOB TEST: (NONE)
    def test_logged_in_user_has_no_job_expect_user(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))

        expected_job = 'user'
        actual_job = response.context['job']
        self.assertEqual(expected_job, actual_job)

    # CHECK IF USER HAS CORRECT JOB TEST: (SITE ADMIN)
    def test_logged_in_user__is_superuser__expect_superuser(self):
        user, profile = self.__create_valid_user_and_profile()
        user.is_superuser = True
        user.save()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={
            'pk': profile.pk,
        }))

        expected_job = 'Site Admin'
        actual_job = response.context['job']
        self.assertEqual(expected_job, actual_job)

    # CHECK IF USER HAS CORRECT JOB TEST: (SITE ADMIN)
    # def test_logged_in_user_has_correct_job_expect_coach(self):
    #     user, profile = self.__create_valid_user_and_profile()
    #     self.__create_group_and_add_user(user, 'Coaches')
    #     self.client.login(**self.VALID_USER_CREDENTIALS)
    #
    #     response = self.client.get(reverse('profile details', kwargs={
    #         'pk': profile.pk,
    #     }))
    #
    #     expected_job = 'Coach'
    #     actual_job = response.context['job']
    #     self.assertEqual(expected_job, actual_job)
