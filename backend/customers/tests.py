import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from courses.models import Course
from customers.models import LearningLog, OrderLog


class PersonalCenterMainPageTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='00000000001')
        get_user_model().objects.create_user(phone_number='00000000002')

    def test_main_page_logged_in(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
        response = self.client.get(reverse('api:customers:personal_center_main_page'))
        response_json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('username' in response_json_data)
        self.assertTrue('avatar' in response_json_data)
        self.assertEqual(response_json_data['phone_number'], '00000000001')
        self.assertTrue('reward_coin' in response_json_data)
        self.assertTrue('date_joined' in response_json_data)
        self.client.logout()

    def test_main_page_logged_out(self):
        response = self.client.get(reverse('api:customers:personal_center_main_page'))
        self.assertEqual(response.status_code, 302)

    def test_change_username_no_conflict(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
        response = self.client.post(
            reverse('api:customers:personal_center_change_username'),
            {'username': '00000000003'}
        )
        response_json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json_data['username'], '00000000003')

    def test_change_username_conflict(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
        response = self.client.post(
            reverse('api:customers:personal_center_change_username'),
            {'username': '00000000002'}
        )
        response_json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_json_data['message'], 'This username is already taken.')


class PersonalCenterLogTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='00000000001')
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
            customer=get_user_model().objects.get(phone_number='00000000001'),
            course=Course.objects.get(codename='c1')
        )
        LearningLog.objects.create(
            customer=get_user_model().objects.get(phone_number='00000000001'),
            course=Course.objects.get(codename='c2')
        )
        OrderLog.objects.create(
            customer=get_user_model().objects.get(phone_number='00000000001'),
            course=Course.objects.get(codename='c1'),
            cash_spent=70,
            payment_method=1
        )
        OrderLog.objects.create(
            customer=get_user_model().objects.get(phone_number='00000000001'),
            course=Course.objects.get(codename='c2'),
            cash_spent=50,
            reward_spent=50,
            payment_method=2,
            refunded_at=timezone.now()
        )

    def test_get_learning_log(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))

        response = self.client.post(
            reverse('api:customers:personal_center_learning_log'),
            {'page_limit': 1, 'page': 1}
        )
        response_json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c2')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't2')
        self.assertEqual(response_json_data['content'][0]['expire_time'], None)
        self.assertEqual(response_json_data['count'], 2)

        response = self.client.post(
            reverse('api:customers:personal_center_learning_log'),
            {'page_limit': 1, 'page': 2}
        )
        response_json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c1')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't1')
        self.assertEqual(response_json_data['content'][0]['expire_time'], None)
        self.assertEqual(response_json_data['count'], 2)

    def test_get_order_log(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))

        response = self.client.post(
            reverse('api:customers:personal_center_order_log'),
            {'page_limit': 1, 'page': 1}
        )
        response_json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c2')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't2')
        self.assertEqual(response_json_data['content'][0]['money'], '100.00')
        self.assertTrue(response_json_data['content'][0]['refunded'])
        self.assertEqual(response_json_data['count'], 2)

        response = self.client.post(
            reverse('api:customers:personal_center_order_log'),
            {'page_limit': 1, 'page': 2}
        )
        response_json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c1')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't1')
        self.assertEqual(response_json_data['content'][0]['money'], '70.00')
        self.assertFalse(response_json_data['content'][0]['refunded'])
        self.assertEqual(response_json_data['count'], 2)