from final_project.accounts.helpers import UserAndProfileData
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from final_project.accounts.models import Profile
from final_project.main.models import Post
from final_project.main.tests_main.views.tests_posts import ValidPostData

UserModel = get_user_model()


class PostLikesTests(ValidPostData, UserAndProfileData, django_test.TestCase):
    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return user, profile

    def __create_post_view(self):
        return Post.objects.create(**self.VALID_POST_DATA)

    def __get_response_for_profile(self, post):
        return self.client.get(reverse('like post', kwargs={'pk': post.pk}))

    # def test_view_increases_likes_correctly(self):
    #     user, profile = self.__create_valid_user_and_profile()
    #     self.client.login(**self.VALID_USER_CREDENTIALS)
    #     post = self.__create_post_view(user)
    #     self.client.post(
    #         reverse('edit post', kwargs={'pk': post.pk}),
    #         data={
    #             'title': 'editedtitle',
    #             'picture': 'http://petko.com',
    #             'description': 'post description',
    #             'creator': profile,
    #         }
    #     )
