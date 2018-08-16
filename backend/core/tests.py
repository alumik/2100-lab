import json
import re

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthModuleTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='00000000001')
        get_user_model().objects.create_user(phone_number='00000000010')

    def test_get_verification_code_success(self):
        response = self.client.post(
            reverse('api:core:get-verification-code'),
            {'phone_number': '00000000001'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(bool(re.match(r'\d{6}$', json.loads(response.content)['verification_code'])))

    def test_get_verification_code_fail(self):
        response = self.client.post(
            reverse('api:core:get-verification-code'),
            {'phone_number': 'apple'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Not a valid phone number.')

    def test_get_eula(self):
        response = self.client.get(reverse('api:core:get-eula'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['content'], 'Test EULA.')

    def test_logout(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))

        response = self.client.get(reverse('api:core:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'User logged out.')

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['is_authenticated'])

    def test_old_user_login_success(self):
        session = self.client.session
        session['verification_code'] = '123456'
        session.save()

        response = self.client.post(
            reverse('api:core:authenticate'),
            {'phone_number': '00000000001', 'verification_code': '123456'}
        )
        response_json_data = json.loads(response.content)
        user = get_user_model().objects.get(phone_number='00000000001')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response_json_data['new_customer'])
        self.assertEqual(response_json_data['username'], user.username)
        self.assertTrue('avatar' in response_json_data)

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])

        self.client.logout()

    def test_new_user_login_success(self):
        session = self.client.session
        session['verification_code'] = '111111'
        session.save()

        response = self.client.post(
            reverse('api:core:authenticate'),
            {'phone_number': '00000000002', 'verification_code': '111111'}
        )
        response_json_data = json.loads(response.content)
        user = get_user_model().objects.get(phone_number='00000000002')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_json_data['new_customer'])
        self.assertEqual(response_json_data['username'], user.username)
        self.assertTrue('avatar' in response_json_data)

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])
        self.assertTrue(get_user_model().objects.filter(phone_number='00000000002').exists())

        self.client.logout()

    def test_old_user_login_fail(self):
        session = self.client.session
        session['verification_code'] = '123456'
        session.save()

        response = self.client.post(
            reverse('api:core:authenticate'),
            {'phone_number': '00000000001', 'verification_code': '000000'}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['message'], 'Wrong verification code.')

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['is_authenticated'])

    def test_new_user_login_fail(self):
        session = self.client.session
        session['verification_code'] = '111111'
        session.save()

        response = self.client.post(
            reverse('api:core:authenticate'),
            {'phone_number': '00000000002', 'verification_code': '000000'}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['message'], 'Wrong verification code.')

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['is_authenticated'])
        self.assertFalse(get_user_model().objects.filter(phone_number='00000000002').exists())

    def test_old_user_login_whole_process(self):
        response = self.client.post(
            reverse('api:core:get-verification-code'),
            {'phone_number': '00000000001'}
        )
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:core:authenticate'),
            {'phone_number': '00000000001', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(json.loads(response.content)['new_customer'])

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])

        self.client.logout()

    def test_new_user_login_whole_process(self):
        response = self.client.post(
            reverse('api:core:get-verification-code'),
            {'phone_number': '00000000003'}
        )
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:core:authenticate'),
            {'phone_number': '00000000003', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['new_customer'])

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])
        self.assertTrue(get_user_model().objects.filter(phone_number='00000000003').exists())

        self.client.logout()

    def test_account_deletion(self):
        first_user = get_user_model().objects.get(phone_number='00000000010')
        first_user_id = first_user.id
        self.client.force_login(first_user)

        response = self.client.delete(reverse('api:core:delete-customer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'Account deleted.')

        response = self.client.post(
            reverse('api:core:get-verification-code'),
            {'phone_number': '00000000010'}
        )
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:core:authenticate'),
            {'phone_number': '00000000010', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['new_customer'])
        second_user_id = get_user_model().objects.get(phone_number='00000000010').id
        self.assertNotEqual(second_user_id, first_user_id)

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])

        response = self.client.delete(reverse('api:core:delete-customer'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'Account deleted.')

        response = self.client.post(
            reverse('api:core:get-verification-code'),
            {'phone_number': '00000000010'}
        )
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:core:authenticate'),
            {'phone_number': '00000000010', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['new_customer'])
        third_user_id = get_user_model().objects.get(phone_number='00000000010').id
        self.assertNotEqual(third_user_id, second_user_id)

        response = self.client.get(reverse('api:core:is-authenticated'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json.loads(response.content)['is_authenticated'])

        self.client.logout()
