import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse


class AdminListTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13300000000')
        get_user_model().objects.create_user(
            phone_number='14400000000',
            password='123456',
            is_staff=True
        )
        get_user_model().objects.create_user(
            phone_number='15500000000',
            password='123456',
            is_staff=True,
            is_superuser=True
        )

    def test_admin_list_denied(self):
        self.client.login(phone_number='14400000000', password='123456')

        response = self.client.get(
            reverse('api:admins:backstage:get-admin-list'),
            {
                'username': '',
                'phone_number': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Access denied.')

    def test_admin_list_success(self):
        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.get(phone_number='14400000000')

        response = self.client.get(
            reverse('api:admins:backstage:get-admin-list'),
            {
                'username': '',
                'phone_number': '',
                'page': 2,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'username': '',
                'phone_number': '',
                'count': 2,
                'page': 2,
                'num_pages': 2,
                'content': [
                    {
                        'admin_id': admin.id,
                        'username': admin.username,
                        'phone_number': admin.phone_number
                    }
                ]
            }
        )


class AdminDetailTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            phone_number='15500000000',
            password='123456',
            is_staff=True,
            is_superuser=True
        )

    def test_admin_detail(self):
        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.get(phone_number='15500000000')

        response = self.client.get(
            reverse('api:admins:backstage:get-admin-detail'),
            {
                'admin_id': admin.id
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'admin_id': admin.id,
                'username': admin.username,
                'phone_number': admin.phone_number,
                'date_joined': response_json_data['date_joined'],
                'updated_at': response_json_data['updated_at'],
                'admin_groups': [
                    'super_admin'
                ]
            }
        )


class AdminOperationsTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            phone_number='14400000000',
            password='123456',
            is_staff=True,
            is_superuser=True
        )
        get_user_model().objects.create_user(
            phone_number='15500000000',
            password='123456',
            is_staff=True,
            is_superuser=True
        )

    def test_change_admin_username_conflict(self):
        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.get(phone_number='14400000000')

        response = self.client.post(
            reverse('api:admins:backstage:change-admin-username'),
            {
                'admin_id': admin.id,
                'new_username': '15500000000'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)['message'],
            'This username is already taken.'
        )

    def test_change_admin_username_invalid(self):
        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.get(phone_number='14400000000')

        response = self.client.post(
            reverse('api:admins:backstage:change-admin-username'),
            {
                'admin_id': admin.id,
                'new_username': 'hello_deleted_'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Invalid username.')

    def test_change_admin_success(self):
        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.get(phone_number='14400000000')

        response = self.client.post(
            reverse('api:admins:backstage:change-admin-username'),
            {
                'admin_id': admin.id,
                'new_username': 'hello'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['new_username'], 'hello')
        admin = get_user_model().objects.get(phone_number='14400000000')
        self.assertEqual(admin.username, 'hello')

    def test_change_admin_password(self):
        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.get(phone_number='14400000000')

        response = self.client.post(
            reverse('api:admins:backstage:change-admin-password'),
            {
                'admin_id': admin.id,
                'new_password': '100000'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'Success.')
        login_state = self.client.login(phone_number='14400000000', password='100000')
        self.assertTrue(login_state)

    def test_delete_admin(self):
        get_user_model().objects.create_user(
            phone_number='16600000000',
            password='123456',
            is_staff=True,
            is_superuser=True
        )

        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.get(phone_number='16600000000')

        response = self.client.post(
            reverse('api:admins:backstage:delete-admin'),
            {'admin_id': admin.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'Object deleted.')
        login_state = self.client.login(phone_number='16600000000', password='123456')
        self.assertFalse(login_state)

    def test_add_admin_conflict(self):
        self.client.login(phone_number='15500000000', password='123456')

        response = self.client.post(
            reverse('api:admins:backstage:add-admin'),
            {
                'phone_number': '15500000000',
                'password': '123456'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Admin is already registered.')

    def test_add_admin_invalid_phone_number(self):
        self.client.login(phone_number='15500000000', password='123456')

        response = self.client.post(
            reverse('api:admins:backstage:add-admin'),
            {
                'phone_number': 'apple',
                'password': '123456'
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Not a valid phone number.')

    def test_add_admin_invalid_password(self):
        self.client.login(phone_number='15500000000', password='123456')

        response = self.client.post(
            reverse('api:admins:backstage:add-admin'),
            {
                'phone_number': '17712345678',
                'password': ''
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'Invalid password.')

    def test_add_admin_success(self):
        self.client.login(phone_number='15500000000', password='123456')

        response = self.client.post(
            reverse('api:admins:backstage:add-admin'),
            {
                'phone_number': '17700000000',
                'password': '123456'
            }
        )
        self.assertEqual(response.status_code, 200)
        new_admin = get_user_model().objects.get(phone_number='17700000000')
        self.assertEqual(json.loads(response.content)['new_admin_id'], new_admin.id)


class AdminGroupsTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            phone_number='15500000000',
            password='123456',
            is_staff=True,
            is_superuser=True
        )

        course_admin = Group.objects.create(name='course_admin')
        comment_admin = Group.objects.create(name='comment_admin')
        customer_admin = Group.objects.create(name='customer_admin')
        order_admin = Group.objects.create(name='order_admin')
        log_admin = Group.objects.create(name='log_admin')

        course_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='course')))
        course_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='hero')))
        course_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='image')))
        comment_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='comment')))
        customer_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='customuser')))
        customer_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='learninglog')))
        order_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='orderlog')))
        log_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='adminlog')))

        course_admin.save()
        comment_admin.save()
        customer_admin.save()
        order_admin.save()
        log_admin.save()

    def test_change_permission(self):
        self.client.login(phone_number='15500000000', password='123456')
        admin = get_user_model().objects.create_user(
            phone_number='14400000000',
            password='123456',
            is_staff=True
        )
        admin.groups.add(Group.objects.get(name='course_admin'))
        admin.save()

        response = self.client.post(
            reverse('api:admins:backstage:change-admin-groups'),
            {
                'admin_id': admin.id,
                'new_admin_groups': [
                    'log_admin',
                    'customer_admin'
                ]
            }
        )
        admin = get_user_model().objects.get(phone_number='14400000000')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Group.objects.get(name='log_admin') in admin.groups.all())
        self.assertTrue(Group.objects.get(name='customer_admin') in admin.groups.all())
        self.assertFalse(Group.objects.get(name='course_admin') in admin.groups.all())
        self.assertFalse(admin.is_superuser)

        response = self.client.post(
            reverse('api:admins:backstage:change-admin-groups'),
            {
                'admin_id': admin.id,
                'new_admin_groups': [
                    'course_admin',
                ]
            }
        )
        admin = get_user_model().objects.get(phone_number='14400000000')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Group.objects.get(name='log_admin') in admin.groups.all())
        self.assertFalse(Group.objects.get(name='customer_admin') in admin.groups.all())
        self.assertTrue(Group.objects.get(name='course_admin') in admin.groups.all())
