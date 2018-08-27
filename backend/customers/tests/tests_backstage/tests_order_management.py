import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from courses.models import Course
from customers.models import OrderLog


class OrderListTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='11122223333', password='123456')
        admin = get_user_model().objects.create_user(phone_number='11122224444', password='123456')
        permission = Permission.objects.get(codename='view_orderlog')
        admin_group = Group.objects.create(name='order_admin')
        admin_group.permissions.add(permission)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()
        course_1 = Course.objects.create(
            title='t1',
            description='d1',
            codename='SOFT1'
        )
        course_2 = Course.objects.create(
            title='t2',
            description='d2',
            codename='SOFT2'
        )
        OrderLog.objects.create(
            order_no='AA01',
            customer=get_user_model().objects.get(phone_number='11122223333'),
            course=course_1,
            cash_spent=70,
            payment_method=1
        )
        OrderLog.objects.create(
            order_no='AA02',
            customer=get_user_model().objects.get(phone_number='11122223333'),
            course=course_2,
            cash_spent=50,
            reward_spent=50,
            payment_method=2,
            refunded_at=timezone.now()
        )

    def test_order_list_access_denied(self):
        self.client.login(phone_number='11122223333', password='123456')

        response = self.client.get(
            reverse('api:customers:backstage:get-order-list'),
            {
                'order_no': '',
                'course_codename': '',
                'course_title': '',
                'customer_username': '',
                'is_refunded': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_order_list_no_filter(self):
        self.client.login(phone_number='11122224444', password='123456')

        response = self.client.get(
            reverse('api:customers:backstage:get-order-list'),
            {
                'order_no': '',
                'course_codename': '',
                'course_title': '',
                'customer_username': '',
                'is_refunded': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['content'][0]['order_no'], 'AA02')
        self.assertEqual(response_json_data['count'], 2)

    def test_order_list_refunded(self):
        self.client.login(phone_number='11122224444', password='123456')

        response = self.client.get(
            reverse('api:customers:backstage:get-order-list'),
            {
                'order_no': '',
                'course_codename': '',
                'course_title': '',
                'customer_username': '',
                'is_refunded': '2',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['content'][0]['order_no'], 'AA02')
        self.assertEqual(response_json_data['count'], 1)


class OrderDetailTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='11122223333', password='123456')
        admin = get_user_model().objects.create_user(phone_number='11122224444', password='123456')
        permission_1 = Permission.objects.get(codename='view_orderlog')
        permission_2 = Permission.objects.get(codename='change_orderlog')
        admin_group = Group.objects.create(name='order_admin')
        admin_group.permissions.add(permission_1, permission_2)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()
        course_1 = Course.objects.create(
            title='t1',
            description='d1',
            codename='SOFT1'
        )
        course_2 = Course.objects.create(
            title='t2',
            description='d2',
            codename='SOFT2'
        )
        OrderLog.objects.create(
            order_no='AA01',
            customer=get_user_model().objects.get(phone_number='11122223333'),
            course=course_1,
            cash_spent=70,
            reward_spent=10,
            payment_method=1
        )
        OrderLog.objects.create(
            order_no='AA02',
            customer=get_user_model().objects.get(phone_number='11122223333'),
            course=course_2,
            cash_spent=50,
            reward_spent=50,
            payment_method=2,
            refunded_at=timezone.now()
        )

    def test_order_detail_not_refunded(self):
        self.client.login(phone_number='11122224444', password='123456')
        order = OrderLog.objects.get(order_no='AA01')

        response = self.client.get(
            reverse('api:customers:backstage:get-order-detail'),
            {'order_id': order.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertFalse(response_json_data['is_refunded'])
        self.assertEqual(response_json_data['order_no'], 'AA01')

    def test_order_detail_refunded(self):
        self.client.login(phone_number='11122224444', password='123456')
        order = OrderLog.objects.get(order_no='AA02')

        response = self.client.get(
            reverse('api:customers:backstage:get-order-detail'),
            {'order_id': order.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertTrue(response_json_data['is_refunded'])
        self.assertEqual(response_json_data['order_no'], 'AA02')

    def test_order_refund(self):
        self.client.login(phone_number='11122224444', password='123456')
        order = OrderLog.objects.get(order_no='AA01')

        response = self.client.post(
            reverse('api:customers:backstage:order-refund'),
            {'order_id': order.id}
        )
        self.assertEqual(response.status_code, 200)
        order = OrderLog.objects.get(order_no='AA01')
        user = get_user_model().objects.get(phone_number='11122223333')
        self.assertTrue(order.refunded_at is not None)
        self.assertEqual(int(user.reward_coin), 10)
