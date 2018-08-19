import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AdminAuthTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            phone_number='13312345678',
            password='nkcs1612',
            is_staff=True
        )
        get_user_model().objects.create_user(
            phone_number='14412345678',
            password='nkcs1612',
        )

    def test_admin_login_wrong_password(self):
        response = self.client.post(
            reverse('api:admins:authenticate-admin'),
            {
                'phone_number': '13312345678',
                'password': '123456'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Wrong phone number or password.')

    def test_admin_login_already_logged_in(self):
        self.client.login(phone_number='13312345678', password='nkcs1612')

        response = self.client.post(
            reverse('api:admins:authenticate-admin'),
            {
                'phone_number': '13312345678',
                'password': 'nkcs1612'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'User is already authenticated.')

        self.client.logout()

    def test_admin_login_success(self):
        admin = get_user_model().objects.get(phone_number='13312345678')

        response = self.client.post(
            reverse('api:admins:authenticate-admin'),
            {
                'phone_number': '13312345678',
                'password': 'nkcs1612'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'permissions': [],
                'admin_id': admin.id,
                'username': admin.username
            }
        )

        self.client.logout()

    def test_admin_login_permission_denied(self):
        response = self.client.post(
            reverse('api:admins:authenticate-admin'),
            {
                'phone_number': '14412345678',
                'password': 'nkcs1612'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Permission denied.')