import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class CoreModuleTests(TestCase):
    def test_logout(self):
        get_user_model().objects.create_user(phone_number='13312345678')
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(reverse('api:core:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'User logged out.')

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['is_authenticated'])
