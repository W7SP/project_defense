from final_project.accounts.helpers import UserAndProfileData
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from final_project.accounts.helpers import UserAndProfileData
from final_project.accounts.models import Profile
from final_project.main.models import Post
from final_project.main.tests_main.views.tests_posts import ValidPostData

UserModel = get_user_model()


class CreatePostViewTests(ValidPostData, UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'posts/create_post.html'

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __get_response_for_profile(self):
        return self.client.get(reverse('create post'))

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

    def test_view_creates_post_correctly(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.client.post(
            reverse('create post'),
            data={
                **self.VALID_POST_DATA,
                'creator': profile,
            }
        )

        post = Post.objects.first()
        self.assertIsNotNone(post.pk)
        self.assertEqual(user, post.creator)

