import json
import uuid
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from courses.models import Course
from customers.models import OrderLog, LearningLog


class CustomerListTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='00000000001')
        get_user_model().objects.create_user(phone_number='00000000002', is_vip=True)
        get_user_model().objects.create_user(phone_number='00000000003', is_vip=True, is_banned=True)
        get_user_model().objects.create_user(phone_number='00000000004', is_banned=True)
        admin = get_user_model().objects.create_user(
            phone_number='11122223333',
            password='123456',
            is_staff=True
        )
        permission = Permission.objects.get(codename='view_customuser')
        admin_group = Group.objects.create(name='customer_admin')
        admin_group.permissions.add(permission)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()

    def test_customer_list_access_denied(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))

        response = self.client.get(
            reverse('api:customers:backstage:get-customer-list'),
            {
                'customer_id': '',
                'username': '',
                'phone_number': '',
                'is_vip': '',
                'is_banned': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_customer_list_no_filter(self):
        self.client.login(phone_number='11122223333', password='123456')

        response = self.client.get(
            reverse('api:customers:backstage:get-customer-list'),
            {
                'customer_id': '',
                'username': '',
                'phone_number': '',
                'is_vip': '',
                'is_banned': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['content'][0]['phone_number'], '00000000004')
        self.assertEqual(response_json_data['count'], 4)

    def test_customer_list_banned_vip(self):
        self.client.login(phone_number='11122223333', password='123456')

        response = self.client.get(
            reverse('api:customers:backstage:get-customer-list'),
            {
                'customer_id': '',
                'username': '',
                'phone_number': '',
                'is_vip': '2',
                'is_banned': '2',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['content'][0]['phone_number'], '00000000003')
        self.assertEqual(response_json_data['count'], 1)


class CustomerDetailTests(TestCase):
    def setUp(self):
        customer = get_user_model().objects.create_user(phone_number='00000000001', is_vip=True, is_banned=True)
        admin = get_user_model().objects.create_user(
            phone_number='11122223333',
            password='123456',
            is_staff=True
        )
        permission = Permission.objects.get(codename='view_customuser')
        admin_group = Group.objects.create(name='customer_admin')
        admin_group.permissions.add(permission)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()
        course = Course.objects.create(
            title='t1',
            codename='c1',
            description='d1'
        )
        LearningLog.objects.create(
            customer=customer,
            course=course
        )
        OrderLog.objects.create(
            order_no=uuid.uuid1(),
            customer=customer,
            course=course,
            cash_spent=70,
            payment_method=1
        )

    def test_customer_detail(self):
        self.client.login(phone_number='11122223333', password='123456')
        customer = get_user_model().objects.get(phone_number='00000000001')

        response = self.client.get(
            reverse('api:customers:backstage:get-customer-detail'),
            {'customer_id': customer.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['customer_info']['username'], '00000000001')
        self.assertEqual(len(response_json_data['recent_orders']), 1)
        self.assertEqual(len(response_json_data['recent_learning_logs']), 1)

    def test_customer_order_list(self):
        self.client.login(phone_number='11122223333', password='123456')
        customer = get_user_model().objects.get(phone_number='00000000001')

        response = self.client.get(
            reverse('api:customers:backstage:get-customer-order-list'),
            {'customer_id': customer.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 1)

    def test_customer_learning_log_list(self):
        self.client.login(phone_number='11122223333', password='123456')
        customer = get_user_model().objects.get(phone_number='00000000001')

        response = self.client.get(
            reverse('api:customers:backstage:get-customer-learning-log-list'),
            {'customer_id': customer.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 1)


class CustomerOperationTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='00000000001', is_vip=True, is_banned=False)
        admin = get_user_model().objects.create_user(
            phone_number='11122223333',
            password='123456',
            is_staff=True
        )
        permission = Permission.objects.get(codename='change_customuser')
        admin_group = Group.objects.create(name='customer_admin')
        admin_group.permissions.add(permission)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()

    def test_toggle_vip(self):
        self.client.login(phone_number='11122223333', password='123456')
        customer = get_user_model().objects.get(phone_number='00000000001')
        response = self.client.post(
            reverse('api:customers:backstage:toggle-vip'),
            {'customer_id': customer.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        customer = get_user_model().objects.get(phone_number='00000000001')
        self.assertFalse(response_json_data['is_vip'])
        self.assertFalse(customer.is_vip)

    def test_toggle_banned(self):
        self.client.login(phone_number='11122223333', password='123456')
        customer = get_user_model().objects.get(phone_number='00000000001')
        response = self.client.post(
            reverse('api:customers:backstage:toggle-banned'),
            {'customer_id': customer.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        customer = get_user_model().objects.get(phone_number='00000000001')
        self.assertTrue(response_json_data['is_banned'])
        self.assertTrue(customer.is_banned)

    def delete_user(self):
        self.client.login(phone_number='11122223333', password='123456')
        customer = get_user_model().objects.create_user(phone_number='00000000002')
        response = self.client.post(
            reverse('api:customers:backstage:delete-customer'),
            {'customer_id': customer.id}
        )
        self.assertEqual(response.status_code, 200)
        customer = get_user_model().objects.create_user(phone_number='00000000002')
        self.assertTrue(bool(re.match(r'.*_deleted_.*', customer.username)))
