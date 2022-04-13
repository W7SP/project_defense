from django.contrib.contenttypes.models import ContentType

from final_project.accounts.helpers import UserAndProfileData
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group, Permission

from final_project.accounts.models import Profile
from final_project.main.models import StudyBook

UserModel = get_user_model()


class BuyBookTests(UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'marketplace/buy_book.html'

    VALID_STUDYBOOK_DATA = {
        'name': 'Atomic Habits',
        'price': 10,
        'cover': 'http://petko.com',
        'description': 'cool book description',
        'link_to_online_book': 'http://petko.com',
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

    def __get_response_for_profile(self, book):
        return self.client.get(reverse('buy book', kwargs={'pk': book.pk}))

    def __create_book_with_author(self, user):
        book = StudyBook.objects.create(**self.VALID_STUDYBOOK_DATA, author=user)
        return book

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        user, _ = self.__create_valid_user_and_profile()
        book = self.__create_book_with_author(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(book)

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        user, _ = self.__create_valid_user_and_profile()
        book = self.__create_book_with_author(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(book)
        self.assertEqual(200, response.status_code)

    # CHECK IF PROFILE CAN BUY BOOK WITH ENOUGH BUDGET CORRECTLY
    def test_user_can_buy_book_with_enough_budget__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        starting_budget = profile.account_balance
        book = self.__create_book_with_author(user)
        expected_budget = starting_budget - book.price
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.client.post(
            reverse('buy book', kwargs={'pk': book.pk}),
            data={
                'owners': profile,
            }
        )
        bought_book = StudyBook.objects.get(owners=profile)
        owner = Profile.objects.get(pk=profile.pk)
        budget_after_buying_the_book = owner.account_balance
        expected_owner = profile

        self.assertEqual(expected_owner, bought_book.owners.first())
        self.assertEqual(expected_budget, budget_after_buying_the_book)

    # CHECK IF PROFILE CAN'T BUY BOOK WITHOUT ENOUGH BUDGET CORRECTLY
    def test_user_can_not_buy_book_without_enough_budget__expect_error_message(self):
        user, profile = self.__create_valid_user_and_profile()
        starting_budget = profile.account_balance
        book = self.__create_book_with_author(user)
        book.price = 1000
        book.save()

        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(
            reverse('buy book', kwargs={'pk': book.pk}),
            data={
                'owners': profile,
            }
        )

        expected_owner = None
        actual_owner = book.owners.first()
        self.assertEqual(expected_owner, actual_owner)

        expected_error_message = b"You can't afford to buy this book"
        self.assertEqual(expected_error_message, response.content)

        self.assertEqual(starting_budget, profile.account_balance)
