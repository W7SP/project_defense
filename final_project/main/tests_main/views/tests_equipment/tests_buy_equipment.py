from datetime import date

from final_project.accounts.helpers import UserAndProfileData
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse
from final_project.accounts.models import Profile
from final_project.main.models import Equipment
from final_project.main.tests_main.views.tests_equipment.init import ValidEquipmentData

UserModel = get_user_model()


class BuyEquipmentTests(ValidEquipmentData, UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'marketplace/buy_equipment.html'

    USER_TO_BUY_EQUIPMENT = {
        'email': 'petko1.adm@abv.bg',
        'password': '1234',
    }

    PROFILE_TO_BUY_EQUIPMENT = {
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

    def __get_response_for_profile(self, equipment):
        return self.client.get(reverse('buy equipment', kwargs={'pk': equipment.pk}))

    def __create_equipment_with_seller(self, user):
        equipment = Equipment.objects.create(**self.VALID_EQUIPMENT_DATA, seller=user)
        return equipment

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        user, _ = self.__create_valid_user_and_profile(self.VALID_USER_CREDENTIALS, self.VALID_PROFILE_DATA)
        equipment = self.__create_equipment_with_seller(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(equipment)

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        user, _ = self.__create_valid_user_and_profile(self.VALID_USER_CREDENTIALS, self.VALID_PROFILE_DATA)
        equipment = self.__create_equipment_with_seller(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(equipment)
        self.assertEqual(200, response.status_code)

    # CHECK IF PROFILE CAN BUY EQUIPMENT WITH ENOUGH BUDGET CORRECTLY
    def test_user_can_buy_equipment_with_enough_budget__expect_success(self):
        """prepare seller information: account balance before and after selling"""
        seller, seller_profile = self.__create_valid_user_and_profile(self.VALID_USER_CREDENTIALS,
                                                                    self.VALID_PROFILE_DATA)
        equipment = self.__create_equipment_with_seller(seller)
        budget_before_selling = seller_profile.account_balance
        expected_budget_for_seller = budget_before_selling + equipment.price

        """prepare user(buyer) information: account balance before and after buying"""
        buyer, buyer_profile = self.__create_valid_user_and_profile(self.USER_TO_BUY_EQUIPMENT,
                                                                    self.PROFILE_TO_BUY_EQUIPMENT)
        budget_before_buying = buyer_profile.account_balance
        expected_budget_for_owner = budget_before_buying - equipment.price

        self.client.login(**self.USER_TO_BUY_EQUIPMENT)

        self.client.post(
            reverse('buy equipment', kwargs={'pk': equipment.pk}),
            data={
                'owners': buyer_profile,
            }
        )

        bought_equipment = Equipment.objects.get(owners=buyer_profile)
        actual_owner = bought_equipment.owners.first()

        """check if owner is set correctly"""
        self.assertEqual(buyer_profile, actual_owner)

        """check if owner's budget decreases with course price correctly"""
        self.assertEqual(expected_budget_for_owner, actual_owner.account_balance)

        """check if seller's budget increases course price correctly"""
        seller_id = bought_equipment.seller.id
        actual_seller_budget = Profile.objects.get(pk=seller_id).account_balance
        self.assertEqual(expected_budget_for_seller, actual_seller_budget)

    # CHECK IF PROFILE CAN'T BUY COURSE WITHOUT ENOUGH BUDGET CORRECTLY
    def test_user_can_not_buy_book_without_enough_budget__expect_error_message(self):
        seller, seller_profile = self.__create_valid_user_and_profile(self.VALID_USER_CREDENTIALS,
                                                                    self.VALID_PROFILE_DATA)
        equipment = self.__create_equipment_with_seller(seller)
        budget_before_selling = seller_profile.account_balance
        equipment.price = 1000
        equipment.save()

        buyer, buyer_profile = self.__create_valid_user_and_profile(self.USER_TO_BUY_EQUIPMENT, self.PROFILE_TO_BUY_EQUIPMENT)
        budget_before_buying = buyer_profile.account_balance
        self.client.login(**self.USER_TO_BUY_EQUIPMENT)

        response = self.client.post(
            reverse('buy equipment', kwargs={'pk': equipment.pk}),
            data={
                'owners': buyer_profile,
            }
        )

        """check if owner didn't set, because account balance wasn't sufficient"""
        expected_owner = None
        actual_owner = equipment.owners.first()
        expected_error_message = b"You can't afford to buy this equipment!"
        self.assertEqual(expected_owner, actual_owner)
        self.assertEqual(expected_error_message, response.content)

        """check if seller's budget hasn't changed"""
        self.assertEqual(budget_before_selling, seller_profile.account_balance)

        """check if buyer's budget hasn't changed"""
        profile_with_not_enough_budget = Profile.objects.get(pk=buyer_profile.pk)
        actual_profile_budget = profile_with_not_enough_budget.account_balance
        self.assertEqual(budget_before_buying, actual_profile_budget)
