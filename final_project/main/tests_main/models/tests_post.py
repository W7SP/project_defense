from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from final_project.main.models import Post

UserModel = get_user_model()


class PostTests(TestCase):
    # SET UP
    VALID_CREATOR_CREDENTIALS = {
        'email': 'petko.adm@abv.bg',
        'password': '123',
    }

    VALID_POST_DATA = {
        'title': 'SOMEPOST',
        'description': 'Some random post in Omnia',
        'picture': 'http://petko.com',
        'date_posted': date(2000, 4, 28),

    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __add_creator_to_post(self, post):
        valid_creator = self.__create_user(**self.VALID_CREATOR_CREDENTIALS)
        post.creator = valid_creator
        post.save()
        return post

    # CREATE COURSE SUCCESS
    def test_course_create__when_all_data_is_valid__expect_success(self):
        post = Post.objects.create(**self.VALID_POST_DATA)
        post = self.__add_creator_to_post(post)

        self.assertIsNotNone(post.pk)
