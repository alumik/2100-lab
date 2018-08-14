from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import json


class PersonalCenterMainPageTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='00000000001')
        get_user_model().objects.create_user(phone_number='00000000002')

    def test_main_page_logged_in(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
        response = self.client.get(reverse('api:customers:personal_center_main_page'))
        response_json_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('username' in response_json_data)
        self.assertTrue('avatar' in response_json_data)
        self.assertEquals(response_json_data['phone_number'], '00000000001')
        self.assertTrue('reward_coin' in response_json_data)
        self.assertTrue('date_joined' in response_json_data)
        self.client.logout()

    def test_main_page_logged_out(self):
        response = self.client.get(reverse('api:customers:personal_center_main_page'))
        self.assertEquals(response.status_code, 302)

    def test_change_username_no_conflict(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
        response = self.client.post(
            reverse('api:customers:personal_center_change_username'),
            {
                'username': '0000000003',
            }
        )
        response_json_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response_json_data['username'], '00000000003')

    def test_change_username_conflict(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
        response = self.client.post(
            reverse('api:customers:personal_center_change_username'),
            {
                'username': '00000000002',
            }
        )
        response_json_data = json.loads(response.content)
        self.assertEquals(response.status_code, 403)
        self.assertTrue(response_json_data['message'], 'This username is already taken.')
