from final_project.accounts.helpers import UserAndProfileData
from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse
from final_project.accounts.models import Profile
from final_project.main.models import Equipment

UserModel = get_user_model()


class BuyEquipmentTests(UserAndProfileData, django_test.TestCase):
    EXPECTED_TEMPLATE = 'marketplace/buy_equipment.html'

    VALID_EQUIPMENT_DATA = {
        'name': 'yoga math',
        'picture': 'http://petko.com',
        'price': 10,
        'description': 'epic yoga amth best buy',
        'warranty': 2,
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

    def __get_response_for_profile(self, equipment):
        return self.client.get(reverse('buy equipment', kwargs={'pk': equipment.pk}))

    def __create_equipment_with_seller(self, user):
        equipment = Equipment.objects.create(**self.VALID_EQUIPMENT_DATA, seller=user)
        return equipment

    # CHECK IF VIEW LOADS CORRECT TEMPLATE
    def test_view_renders_correct_template(self):
        user, _ = self.__create_valid_user_and_profile()
        equipment = self.__create_equipment_with_seller(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(equipment)

        self.assertTemplateUsed(response, self.EXPECTED_TEMPLATE)

    # CHECK IF VIEW IS ACCESSED ONLY BY LOGGED-IN USER
    def test_when_opening_with_logged_in_user__expect_200(self):
        user, _ = self.__create_valid_user_and_profile()
        equipment = self.__create_equipment_with_seller(user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.__get_response_for_profile(equipment)

        self.assertEqual(200, response.status_code)

    # CHECK IF PROFILE CAN BUY EQUIPMENT WITH ENOUGH BUDGET CORRECTLY
    def test_user_can_buy_equipment_with_enough_budget__expect_success(self):
        user, profile = self.__create_valid_user_and_profile()
        starting_budget = profile.account_balance
        equipment = self.__create_equipment_with_seller(user)
        expected_budget = starting_budget - equipment.price
        self.client.login(**self.VALID_USER_CREDENTIALS)

        self.client.post(
            reverse('buy equipment', kwargs={'pk': equipment.pk}),
            data={
                'owners': profile,
            }
        )

        bought_equipment = Equipment.objects.get(owners=profile)
        owner = Profile.objects.get(pk=profile.pk)
        budget_after_buying_the_equipment = owner.account_balance
        expected_owners = profile

        self.assertEqual(expected_owners, bought_equipment.owners.first())
        self.assertEqual(expected_budget, budget_after_buying_the_equipment)

    # CHECK IF PROFILE CAN'T BUY EQUIPMENT WITHOUT ENOUGH BUDGET CORRECTLY
    def test_user_can_not_equipment_book_without_enough_budget__expect_error_message(self):
        user, profile = self.__create_valid_user_and_profile()
        starting_budget = profile.account_balance
        equipment = self.__create_equipment_with_seller(user)
        equipment.price = 1000
        equipment.save()

        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(
            reverse('buy equipment', kwargs={'pk': equipment.pk}),
            data={
                'owners': profile,
            }
        )

        expected_owner = None
        actual_owner = equipment.owners.first()
        self.assertEqual(expected_owner, actual_owner)

        expected_error_message = b"You can't afford to buy this equipment!"
        self.assertEqual(expected_error_message, response.content)

        self.assertEqual(starting_budget, profile.account_balance)