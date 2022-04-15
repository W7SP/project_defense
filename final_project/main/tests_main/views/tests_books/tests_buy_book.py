from datetime import date

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


class BuyBookTests(ValidStudyBookData, UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'marketplace/buy_book.html'

    USER_TO_BUY_BOOK = {
        'email': 'petko1.adm@abv.bg',
        'password': '1234',
    }

    PROFILE_TO_BUY_BOOK = {
            'first_name': 'Petko2',
            'last_name': 'Stankov2',
            'picture': 'http://petko.com',
            'date_of_birth': date(2000, 4, 28),
            'gender': 'male',
            'account_balance': 100,
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self, user_credentials, profile_info):
        user = self.__create_user(**user_credentials)
        profile = Profile.objects.create(
            **profile_info,
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
        user, _ = self.__create_valid_user_and_profile(self.VALID_USER_CREDENTIALS, self.VALID_PROFILE_DATA)
        book = self.__create_book_with_author(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(book)

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        user, _ = self.__create_valid_user_and_profile(self.VALID_USER_CREDENTIALS, self.VALID_PROFILE_DATA)
        book = self.__create_book_with_author(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(book)
        self.assertEqual(200, response.status_code)

    # CHECK IF PROFILE CAN BUY BOOK WITH ENOUGH BUDGET CORRECTLY
    def test_user_can_buy_book_with_enough_budget__expect_success(self):
        """prepare author information: account balance before and after selling"""
        author, author_profile = self.__create_valid_user_and_profile(self.VALID_USER_CREDENTIALS, self.VALID_PROFILE_DATA)
        book = self.__create_book_with_author(author)
        budget_before_selling = author_profile.account_balance
        expected_budget_for_seller = budget_before_selling + book.price

        """prepare user(buyer) information: account balance before and after buying"""
        buyer, buyer_profile = self.__create_valid_user_and_profile(self.USER_TO_BUY_BOOK, self.PROFILE_TO_BUY_BOOK)
        budget_before_buying = buyer_profile.account_balance
        expected_budget_for_owner = budget_before_buying - book.price

        self.client.login(**self.USER_TO_BUY_BOOK)

        self.client.post(
            reverse('buy book', kwargs={'pk': book.pk}),
            data={
                'owners': buyer_profile,
            }
        )

        bought_book = StudyBook.objects.get(owners=buyer_profile)
        actual_owner = bought_book.owners.first()

        """check if owner is set correctly"""
        self.assertEqual(buyer_profile, actual_owner)

        """check if owner's budget decreases with book price correctly"""
        self.assertEqual(expected_budget_for_owner, actual_owner.account_balance)

        """check if seller's budget increases book price correctly"""
        seller_id = bought_book.author.id
        actual_seller_budget = Profile.objects.get(pk=seller_id).account_balance
        self.assertEqual(expected_budget_for_seller, actual_seller_budget)

    # CHECK IF PROFILE CAN'T BUY BOOK WITHOUT ENOUGH BUDGET CORRECTLY
    def test_user_can_not_buy_book_without_enough_budget__expect_error_message(self):
        author, author_profile = self.__create_valid_user_and_profile(self.VALID_USER_CREDENTIALS, self.VALID_PROFILE_DATA)
        budget_before_selling = author_profile.account_balance
        book = self.__create_book_with_author(author)
        book.price = 1000
        book.save()

        buyer, buyer_profile = self.__create_valid_user_and_profile(self.USER_TO_BUY_BOOK, self.PROFILE_TO_BUY_BOOK)
        budget_before_buying = buyer_profile.account_balance
        self.client.login(**self.USER_TO_BUY_BOOK)

        response = self.client.post(
            reverse('buy book', kwargs={'pk': book.pk}),
            data={
                'owners': buyer_profile,
            }
        )

        """check if owner didn't set, because account balance wasn't sufficient"""
        expected_owner = None
        actual_owner = book.owners.first()
        expected_error_message = b"You can't afford to buy this book"
        self.assertEqual(expected_owner, actual_owner)
        self.assertEqual(expected_error_message, response.content)

        """check if seller's budget hasn't changed"""
        self.assertEqual(budget_before_selling, author_profile.account_balance)

        """check if buyer's budget hasn't changed"""
        profile_with_not_enough_budget = Profile.objects.get(pk=buyer_profile.pk)
        actual_profile_budget = profile_with_not_enough_budget.account_balance
        self.assertEqual(budget_before_buying, actual_profile_budget)
