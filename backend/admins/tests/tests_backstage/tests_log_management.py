import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class LogListTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            phone_number='11122223333',
            password='123456',
            is_staff=True,
            is_superuser=True
        )

    def test_admin_log(self):
        self.client.login(phone_number='11122223333', password='123456')
        admin = get_user_model().objects.get(phone_number='11122223333')

        response = self.client.post(
            reverse('api:admins:backstage:change-admin-username'),
            {
                'admin_id': admin.id,
                'new_username': 'Tiger'
            }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('api:admins:backstage:get-admin-log'),
            {
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 0)

        response = self.client.get(
            reverse('api:admins:backstage:get-admin-log'),
            {
                'start_timestamp': 1534910804,
                'end_timestamp': 1634910804,
                'filters': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 1)
        self.assertEqual(
            response_json_data['content'][0]['message'],
            '将ID为 ' + str(admin.id) + ' 的管理员的用户名由 11122223333 改为 Tiger'
        )
