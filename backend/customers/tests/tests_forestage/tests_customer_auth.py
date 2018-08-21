import json
import re

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class CustomerAuthTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13312345678')

    def test_get_verification_code(self):
        response = self.client.get(reverse('api:customers:forestage:get-generate-time'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['generate_time'], '')

        response = self.client.post(
            reverse('api:customers:forestage:get-verification-code'),
            {'phone_number': '13312345678'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            bool(
                re.match(r'^\d{6}$', json.loads(response.content)['verification_code'])
            )
        )
        self.assertFalse(json.loads(response.content)['is_new_customer'])

        generate_time = self.client.session['generate_time']
        response = self.client.get(reverse('api:customers:forestage:get-generate-time'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['generate_time'], generate_time)

    def test_get_verification_code_invalid_phone_number(self):
        response = self.client.post(
            reverse('api:customers:forestage:get-verification-code'),
            {'phone_number': 'apple'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Not a valid phone number.')

    def test_get_eula(self):
        response = self.client.get(reverse('api:customers:forestage:get-eula'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['content'], 'Test EULA.')

    def test_old_user_login(self):
        response = self.client.post(
            reverse('api:customers:forestage:get-verification-code'),
            {'phone_number': '13312345678'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['is_new_customer'])
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:customers:forestage:authenticate-customer'),
            {'phone_number': '13312345679', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Different phone number.')

        response = self.client.post(
            reverse('api:customers:forestage:authenticate-customer'),
            {'phone_number': '13312345678', 'verification_code': '0'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Wrong verification code.')

        response = self.client.post(
            reverse('api:customers:forestage:authenticate-customer'),
            {'phone_number': '13312345678', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertFalse(response_json_data['is_new_customer'])
        self.assertEqual(response_json_data['username'], '13312345678')

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])

        self.client.logout()

    def test_new_user_login_whole_process(self):
        response = self.client.post(
            reverse('api:customers:forestage:get-verification-code'),
            {'phone_number': '14412345678'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_new_customer'])
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:customers:forestage:authenticate-customer'),
            {'phone_number': '14412345679', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Different phone number.')

        response = self.client.post(
            reverse('api:customers:forestage:authenticate-customer'),
            {'phone_number': '14412345678', 'verification_code': '0'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Wrong verification code.')

        response = self.client.post(
            reverse('api:customers:forestage:authenticate-customer'),
            {'phone_number': '14412345678', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertTrue(response_json_data['is_new_customer'])
        self.assertEqual(response_json_data['username'], '14412345678')

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])

        self.client.logout()
