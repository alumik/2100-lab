import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from courses.models import Course
from customers.models import LearningLog, OrderLog


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

        response = self.client.get(
            reverse('api:customers:forestage:get-learning-logs'),
            {
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c2')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't2')
        self.assertEqual(response_json_data['content'][0]['expire_time'], None)

        response = self.client.get(
            reverse('api:customers:forestage:get-learning-logs'),
            {
                'page': 2,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c1')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't1')
        self.assertEqual(response_json_data['content'][0]['expire_time'], None)

    def test_get_order_log(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(
            reverse('api:customers:forestage:get-order-logs'),
            {
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['order_no'], 'AA02')
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c2')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't2')
        self.assertEqual(response_json_data['content'][0]['money'], '100.00')
        self.assertTrue(response_json_data['content'][0]['refunded'])

        response = self.client.get(
            reverse('api:customers:forestage:get-order-logs'),
            {
                'page': 2,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['order_no'], 'AA01')
        self.assertEqual(response_json_data['content'][0]['course_codename'], 'c1')
        self.assertEqual(response_json_data['content'][0]['course_title'], 't1')
        self.assertEqual(response_json_data['content'][0]['money'], '70.00')
        self.assertFalse(response_json_data['content'][0]['refunded'])
