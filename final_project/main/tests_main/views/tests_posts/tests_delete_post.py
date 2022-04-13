from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from final_project.accounts.helpers import UserAndProfileData
from final_project.accounts.models import Profile
from final_project.main.models import Post
from final_project.main.tests_main.views.tests_posts import ValidPostData

UserModel = get_user_model()


class DeletePostViewTests(ValidPostData, UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'posts/delete_post.html'

    SECOND_VALID_USER_CREDENTIALS = {
        'email': 'wronguser@abv.bg',
        'password': '1234',
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

    def __create_post_view(self, user):
        return Post.objects.create(**self.VALID_POST_DATA, creator=user)

    def __get_response_for_profile(self, post):
        return self.client.get(reverse('delete post', kwargs={'pk': post.pk}))

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        post = self.__create_post_view(user)
        response = self.__get_response_for_profile(post)

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        post = self.__create_post_view(user)
        response = self.__get_response_for_profile(post)

        self.assertEqual(200, response.status_code)

    # CHECK IF VIEW DELETES POST WITH CORRECT USER
    def test_deleting_post_with_correct_user__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        post = self.__create_post_view(user)

        self.client.post(
            reverse('delete post', kwargs={'pk': post.pk}),
            data={},
        )

        deleted_post = Post.objects.first()

        self.assertIsNone(deleted_post)

    # CHECK IF VIEW DELETES POST WITH WRONG USER
    def test_deleting_post_with_wrong_user__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        post = self.__create_post_view(user)

        wrong_user = self.__create_user(**self.SECOND_VALID_USER_CREDENTIALS)
        self.client.login(**self.SECOND_VALID_USER_CREDENTIALS)

        response = self.client.post(
            reverse('delete post', kwargs={'pk': post.pk}),
            data={},
        )

        not_deleted_post = Post.objects.first()
        error_message = b'You must be the creator to delete the post!'

        self.assertEqual(error_message, response.content)
        self.assertIsNotNone(not_deleted_post)

