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

    def __create_post_view(self, creator):
        return Post.objects.create(**self.VALID_POST_DATA, creator=creator)

    def __get_response_for_profile(self, post):
        return self.client.get(reverse('like post', kwargs={'pk': post.pk}))

    def __post_response_for_view(self, post):
        return self.client.post(
            reverse('like post', kwargs={'pk': post.pk}),
            data={**self.VALID_POST_DATA}
        )

    def test_view_user_can_like_post_once__if_liked_twice_likes_do_not_change_correctly(self):
        post_creator = self.__create_user(**{
                                            'email': 'creator.adm@abv.bg',
                                            'password': '1234',
                                            })
        post = self.__create_post_view(post_creator)

        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        """first like"""
        self.__post_response_for_view(post)
        post = Post.objects.get(pk=post.pk)

        """check if likes increase +1 when user likes first time"""
        expected_likes = 1
        actual_likes = post.likes
        self.assertEqual(expected_likes, actual_likes)

        """second like"""
        self.__post_response_for_view(post)
        post = Post.objects.get(pk=post.pk)
        expected_likes = 0
        actual_likes = post.likes
        self.assertEqual(expected_likes, actual_likes)





