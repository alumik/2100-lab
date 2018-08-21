import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PersonalCenterMainPageTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13312345678', reward_coin='100.00')
        get_user_model().objects.create_user(phone_number='14412345678')

    def test_main_page_logged_in(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(reverse('api:customers:forestage:get-customer-detail'))
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertTrue('avatar' in response_json_data)
        self.assertEqual(response_json_data['username'], '13312345678')
        self.assertEqual(response_json_data['phone_number'], '13312345678')
        self.assertEqual(response_json_data['reward_coin'], '100.00')
        self.assertTrue('date_joined' in response_json_data)

        self.client.logout()

    def test_main_page_logged_out(self):
        response = self.client.get(reverse('api:customers:forestage:get-customer-detail'))
        self.assertEqual(response.status_code, 302)

    def test_change_username_success(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.post(
            reverse('api:customers:forestage:change-username'),
            {'username': 'u1'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['new_username'], 'u1')

    def test_change_username_fail(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.post(
            reverse('api:customers:forestage:change-username'),
            {'username': '13312345678_deleted_2'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Invalid username.')

        response = self.client.post(
            reverse('api:customers:forestage:change-username'),
            {'username': '14412345678'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'This username is already taken.')

    def test_get_reward_coin(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(reverse('api:customers:forestage:get-reward-coin'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['reward_coin'], '100.00')

    def test_delete_customer(self):
        get_user_model().objects.create_user(phone_number='19912345678')
        first_user = get_user_model().objects.get(phone_number='19912345678')
        first_user_id = first_user.id
        self.client.force_login(first_user)

        response = self.client.delete(reverse('api:customers:forestage:delete-customer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'Object deleted.')

        response = self.client.post(
            reverse('api:customers:forestage:get-verification-code'),
            {'phone_number': '19912345678'}
        )
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:customers:forestage:authenticate-customer'),
            {'phone_number': '19912345678', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_new_customer'])
        second_user_id = get_user_model().objects.get(phone_number='19912345678').id
        self.assertNotEqual(second_user_id, first_user_id)

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])

        response = self.client.delete(reverse('api:customers:forestage:delete-customer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'Object deleted.')

        response = self.client.post(
            reverse('api:customers:forestage:get-verification-code'),
            {'phone_number': '19912345678'}
        )
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:customers:forestage:authenticate-customer'),
            {'phone_number': '19912345678', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_new_customer'])
        third_user_id = get_user_model().objects.get(phone_number='19912345678').id
        self.assertNotEqual(third_user_id, second_user_id)

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])

        self.client.logout()
