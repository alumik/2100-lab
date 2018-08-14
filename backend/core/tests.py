from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import json
import re


class AuthModuleTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='12345678901')

    def test_get_verification_code_success(self):
        json_data = json.dumps({'phone_number': '12345678901'})

        response = self.client.post(
            reverse('api:core:get_verification_code'),
            json_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(bool(re.match(r'\d{6}$', json.loads(response.content)['verification_code'])), True)

    def test_get_verification_code_fail(self):
        json_data = json.dumps({'phone_number': 'apple'})

        response = self.client.post(
            reverse('api:core:get_verification_code'),
            json_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Not a valid phone number.')

    def test_get_eula(self):
        response = self.client.get(
            reverse('api:core:get_eula'),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['content'], 'Test EULA.')

    def test_logout(self):
        self.client.force_login(get_user_model().objects.get(phone_number='12345678901'))

        response = self.client.get(
            reverse('api:core:logout'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'User logged out.')

        response = self.client.get(
            reverse('api:core:is_authenticated'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['is_authenticated'], False)

    def test_old_user_login_success(self):
        session = self.client.session
        session['verification_code'] = '123456'
        session.save()
        json_data = json.dumps({'phone_number': '12345678901', 'verification_code': '123456'})

        response = self.client.post(
            reverse('api:core:authenticate'),
            json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['new_user'], False)

        response = self.client.get(
            reverse('api:core:is_authenticated'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['is_authenticated'], True)

        self.client.logout()

    def test_new_user_login_success(self):
        session = self.client.session
        session['verification_code'] = '111111'
        session.save()
        json_data = json.dumps({'phone_number': '11122223333', 'verification_code': '111111'})

        response = self.client.post(
            reverse('api:core:authenticate'),
            json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['new_user'], True)

        response = self.client.get(
            reverse('api:core:is_authenticated'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['is_authenticated'], True)

        self.client.logout()

    def test_old_user_login_fail(self):
        session = self.client.session
        session['verification_code'] = '123456'
        session.save()
        json_data = json.dumps({'phone_number': '1234567890', 'verification_code': '111111'})

        response = self.client.post(
            reverse('api:core:authenticate'),
            json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['message'], 'Wrong verification code.')

        response = self.client.get(
            reverse('api:core:is_authenticated'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['is_authenticated'], False)

    def test_new_user_login_fail(self):
        session = self.client.session
        session['verification_code'] = '123456'
        session.save()
        json_data = json.dumps({'phone_number': '11144443333', 'verification_code': '111111'})

        response = self.client.post(
            reverse('api:core:authenticate'),
            json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['message'], 'Wrong verification code.')

        response = self.client.get(
            reverse('api:core:is_authenticated'),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['is_authenticated'], False)

