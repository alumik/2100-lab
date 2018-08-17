import json
import re

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from courses.models import Course
from customers.models import LearningLog, OrderLog


class CustomerAuthTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13312345678')

    def test_get_verification_code(self):
        response = self.client.post(
            reverse('api:customers:get-verification-code'),
            {'phone_number': '13312345678'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(bool(re.match(r'^\d{6}$', json.loads(response.content)['verification_code'])))

    def test_get_verification_code_invalid_phone_number(self):
        response = self.client.post(
            reverse('api:customers:get-verification-code'),
            {'phone_number': 'apple'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Not a valid phone number.')

    def test_get_eula(self):
        response = self.client.get(reverse('api:customers:get-eula'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['content'], 'Test EULA.')

    def test_old_user_login(self):
        response = self.client.post(
            reverse('api:customers:get-verification-code'),
            {'phone_number': '13312345678'}
        )
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:customers:authenticate-customer'),
            {'phone_number': '13312345679', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['message'], 'Different phone number.')

        response = self.client.post(
            reverse('api:customers:authenticate-customer'),
            {'phone_number': '13312345678', 'verification_code': '0'}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['message'], 'Wrong verification code.')

        response = self.client.post(
            reverse('api:customers:authenticate-customer'),
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
            reverse('api:customers:get-verification-code'),
            {'phone_number': '14412345678'}
        )
        verification_code = json.loads(response.content)['verification_code']

        response = self.client.post(
            reverse('api:customers:authenticate-customer'),
            {'phone_number': '14412345679', 'verification_code': verification_code}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['message'], 'Different phone number.')

        response = self.client.post(
            reverse('api:customers:authenticate-customer'),
            {'phone_number': '14412345678', 'verification_code': '0'}
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content)['message'], 'Wrong verification code.')

        response = self.client.post(
            reverse('api:customers:authenticate-customer'),
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


class PersonalCenterMainPageTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13312345678')
        get_user_model().objects.create_user(phone_number='14412345678')

    def test_main_page_logged_in(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(reverse('api:customers:personal-center-get-customer-detail'))
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertTrue('avatar' in response_json_data)
        self.assertEqual(response_json_data['username'], '13312345678')
        self.assertEqual(response_json_data['phone_number'], '13312345678')
        self.assertEqual(response_json_data['reward_coin'], '0.00')
        self.assertTrue('date_joined' in response_json_data)

        self.client.logout()

    def test_main_page_logged_out(self):
        response = self.client.get(reverse('api:customers:personal-center-get-customer-detail'))
        self.assertEqual(response.status_code, 302)

    def test_change_username_success(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.post(
            reverse('api:customers:personal-center-change-username'),
            {'username': 'u1'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['new_username'], 'u1')

    def test_change_username_fail(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.post(
            reverse('api:customers:personal-center-change-username'),
            {'username': '13312345678_deleted_2'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Invalid username.')

        response = self.client.post(
            reverse('api:customers:personal-center-change-username'),
            {'username': '14412345678'}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'This username is already taken.')


class PersonalCenterLogTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13312345678')
        Course.objects.create(
            title='t1',
            description='d1',
            codename='c1'
        )
        Course.objects.create(
            title='t2',
            description='d2',
            codename='c2'
        )
        LearningLog.objects.create(
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c1')
        )
        LearningLog.objects.create(
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c2')
        )
        OrderLog.objects.create(
            order_no='AA01',
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c1'),
            cash_spent=70,
            payment_method=1
        )
        OrderLog.objects.create(
            order_no='AA02',
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c2'),
            cash_spent=50,
            reward_spent=50,
            payment_method=2,
            refunded_at=timezone.now()
        )

    def test_get_learning_log(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.post(
            reverse('api:customers:personal-center-get-learning-logs') + '?page=1',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c2')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't2')
        self.assertEqual(response_json_data['content'][0]['expire_time'], None)

        response = self.client.post(
            reverse('api:customers:personal-center-get-learning-logs') + '?page=2',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c1')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't1')
        self.assertEqual(response_json_data['content'][0]['expire_time'], None)

    def test_get_order_log(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.post(
            reverse('api:customers:personal-center-get-order-logs') + '?page=1',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['order_no'], 'AA02')
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c2')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't2')
        self.assertEqual(response_json_data['content'][0]['money'], '100.00')
        self.assertTrue(response_json_data['content'][0]['refunded'])

        response = self.client.post(
            reverse('api:customers:personal-center-get-order-logs') + '?page=2',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['order_no'], 'AA01')
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c1')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't1')
        self.assertEqual(response_json_data['content'][0]['money'], '70.00')
        self.assertFalse(response_json_data['content'][0]['refunded'])
