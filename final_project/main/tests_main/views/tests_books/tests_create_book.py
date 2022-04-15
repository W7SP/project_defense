from django.contrib.contenttypes.models import ContentType

from final_project.accounts.helpers import UserAndProfileData
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group, Permission

from final_project.accounts.models import Profile
from final_project.main.models import StudyBook
from final_project.main.tests_main.views.tests_books import ValidStudyBookData

UserModel = get_user_model()


class BookShopTests(ValidStudyBookData, UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'books/create_book.html'

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
        return self.client.get(reverse('create book'))

    def __create_group_and_add_user(self, user, group_name):
        group = Group.objects.get_or_create(name=group_name)
        user.groups.add(group[0])
        user.save()
        return group

    # CHECK IF VIEW ALLOWS ONLY USERS WITH PERMISSION 'ADD_STUDYBOOK' CAN ENTER
    def test_view_allows_only_authorized_users__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        content_type = ContentType.objects.get_for_model(UserModel)
        group = self.__create_group_and_add_user(user, 'Authors')[0]
        permission = Permission.objects.create(
            codename='add_studybook',
            name='can_add_studybook',
            content_type=content_type,
        )

        group.permissions.add(permission)
        group.user_set.add(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(
            reverse('create book'),
            data={
                'name': 'Atomic Habits',
                'price': 10,
                'cover': 'http://petko.com',
                'description': 'cool book description',
                'link_to_online_book': 'http://petko.com',
            },
        )

        self.assertEqual(200, response.status_code)

    # CHECK IF VIEW CREATES A BOOK CORRECTLY
    def test_view_creates_book_successfully(self):
        user, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(
            reverse('create book'),
            data={
                'name': 'Atomic Habits',
                'price': 10,
                'cover': 'http://petko.com',
                'description': 'cool book description',
                'link_to_online_book': 'http://petko.com',
            },
        )

        book = StudyBook.objects.first()
        print(book)