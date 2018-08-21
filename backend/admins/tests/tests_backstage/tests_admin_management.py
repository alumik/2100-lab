import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AdminListTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13300000000')
        get_user_model().objects.create_user(phone_number='14400000000', password='123456', is_staff=True)
        get_user_model().objects.create_user(
            phone_number='15500000000',
            password='123456',
            is_staff=True,
            is_superuser=True
        )

    def test_admin_list_denied(self):
        self.client.login(phone_number='14400000000', password='123456')

        response = self.client.get(
            reverse('api:admins:backstage:get-admin-list'),
            {
                'username': '',
                'phone_number': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Access denied.')

    def test_admin_list_success(self):
        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.get(phone_number='14400000000')

        response = self.client.get(
            reverse('api:admins:backstage:get-admin-list'),
            {
                'username': '',
                'phone_number': '',
                'page': 2,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'username': '',
                'phone_number': '',
                'count': 2,
                'page': 2,
                'num_pages': 2,
                'content': [
                    {
                        'admin_id': admin.id,
                        'username': admin.username,
                        'phone_number': admin.phone_number
                    }
                ]
            }
        )


class AdminDetailTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            phone_number='15500000000',
            password='123456',
            is_staff=True,
            is_superuser=True
        )

    def test_admin_detail(self):
        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.get(phone_number='15500000000')

        response = self.client.get(
            reverse('api:admins:backstage:get-admin-detail'),
            {
                'admin_id': admin.id
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'admin_id': admin.id,
                'username': admin.username,
                'phone_number': admin.phone_number,
                'date_joined': response_json_data['date_joined'],
                'updated_at': response_json_data['updated_at'],
                'roles': [
                    'super_admin'
                ]
            }
        )
