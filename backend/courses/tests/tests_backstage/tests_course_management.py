from decimal import Decimal
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from courses.models import Course, Hero, Image


class CourseListTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='14412345678', password='123456')
        admin = get_user_model().objects.create_user(phone_number='13312345678', password='123456')
        permission = Permission.objects.get(codename='view_course')
        admin_group = Group.objects.create(name='course_admin')
        admin_group.permissions.add(permission)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()
        Course.objects.create(
            title='t1',
            description='d1',
            codename='SOFT1'
        )
        Course.objects.create(
            title='t2',
            description='d2',
            codename='SCIENCE2',
            price='100.00'
        )
        Course.objects.create(
            title='t3',
            description='d3',
            codename='SOFT3'
        )

    def test_course_list_access_denied(self):
        self.client.login(phone_number='14412345678', password='123456')

        response = self.client.get(
            reverse('api:courses:backstage:get-course-list'),
            {
                'codename': '',
                'title': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_course_list_no_filter(self):
        self.client.login(phone_number='13312345678', password='123456')
        course = Course.objects.get(codename='SCIENCE2')

        response = self.client.get(
            reverse('api:courses:backstage:get-course-list'),
            {
                'codename': '',
                'title': '',
                'page': 2,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'codename': '',
                'title': '',
                'count': 3,
                'page': 2,
                'num_pages': 3,
                'content': [
                    {
                        'course_id': course.id,
                        'codename': 'SCIENCE2',
                        'title': 't2',
                        'price': '100.00',
                        'updated_at': response_json_data['content'][0]['updated_at']
                    }
                ]
            }
        )

    def test_course_list_one_filter(self):
        self.client.login(phone_number='13312345678', password='123456')
        course = Course.objects.get(codename='SOFT1')

        response = self.client.get(
            reverse('api:courses:backstage:get-course-list'),
            {
                'codename': 'SOFT',
                'title': '',
                'page': 2,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'codename': 'SOFT',
                'title': '',
                'count': 2,
                'page': 2,
                'num_pages': 2,
                'content': [
                    {
                        'course_id': course.id,
                        'codename': 'SOFT1',
                        'title': 't1',
                        'price': '0.00',
                        'updated_at': response_json_data['content'][0]['updated_at']
                    }
                ]
            }
        )

    def test_course_list_two_filter(self):
        self.client.login(phone_number='13312345678', password='123456')
        course = Course.objects.get(codename='SOFT1')

        response = self.client.get(
            reverse('api:courses:backstage:get-course-list'),
            {
                'codename': 'SOFT',
                'title': '1',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'codename': 'SOFT',
                'title': '1',
                'count': 1,
                'page': 1,
                'num_pages': 1,
                'content': [
                    {
                        'course_id': course.id,
                        'codename': 'SOFT1',
                        'title': 't1',
                        'price': '0.00',
                        'updated_at': response_json_data['content'][0]['updated_at']
                    }
                ]
            }
        )


class CourseDetailTests(TestCase):
    def test_get_course_detail(self):
        admin = get_user_model().objects.create_user(phone_number='13312345678', password='123456')
        permission = Permission.objects.get(codename='view_course')
        admin_group = Group.objects.create(name='course_admin')
        admin_group.permissions.add(permission)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()
        course = Course.objects.create(
            title='t1',
            description='d1',
            codename='SOFT1'
        )
        self.client.login(phone_number='13312345678', password='123456')

        response = self.client.get(
            reverse('api:courses:backstage:get-course-detail'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'course_id': course.id,
                'codename': 'SOFT1',
                'title': 't1',
                'up_votes': course.up_votes.count(),
                'expire_duration': 'P0DT00H00M00S',
                'price': '0.00',
                'reward_percent': '0.00',
                'thumbnail': '',
                'created_at': response_json_data['created_at'],
                'updated_at': response_json_data['updated_at'],
                'description': 'd1',
            }
        )


class CourseOperationsTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            phone_number='13312345678',
            password='123456',
            is_staff=True,
            is_superuser=True
        )

    def test_delete_course(self):
        self.client.login(phone_number='13312345678', password='123456')
        course = Course.objects.create(
            title='t1',
            description='d1',
            codename='SOFT1'
        )

        response = self.client.post(
            reverse('api:courses:backstage:delete-course'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        course = Course.all_objects.get(title='t1')
        self.assertTrue(course.deleted_at is not None)

    def test_add_course(self):
        self.client.login(phone_number='13312345678', password='123456')

        response = self.client.post(
            reverse('api:courses:backstage:add-course'),
            {
                'title': 'test_title1',
                'codename': 'test_codename1',
                'days': 2,
                'hours': 3,
                'price': 23.43,
                'can_comment': 1,
                'reward_percent': 0.50,
                'description': 'test_description1'
            }
        )
        self.assertEqual(response.status_code, 200)
        course = Course.objects.get(codename='test_codename1')
        self.assertEqual(course.title, 'test_title1')
        self.assertTrue(course.can_comment)
        self.assertEqual(course.reward_percent, Decimal('0.50'))

    def test_delete_course_images(self):
        self.client.login(phone_number='13312345678', password='123456')
        course = Course.objects.create(
            title='t1',
            description='d1',
            codename='SOFT1'
        )
        image = Image.objects.create(
            image_path='fake/1.png',
            course=course,
            load_time=1
        )

        response = self.client.get(
            reverse('api:courses:forestage:get-course-assets'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['images']), 1)

        response = self.client.post(
            reverse('api:courses:backstage:delete-course-images'),
            {'delete_list': [image.id]}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('api:courses:forestage:get-course-assets'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['images']), 0)


class HeroOperationsTests(TestCase):
    def test_delete_hero(self):
        get_user_model().objects.create_user(
            phone_number='13312345678',
            password='123456',
            is_staff=True,
            is_superuser=True
        )
        self.client.login(phone_number='13312345678', password='123456')
        hero = Hero.objects.create(
            image='fake/path/image1.png',
            caption='c1'
        )

        response = self.client.post(
            reverse('api:courses:backstage:delete-hero'),
            {
                'delete_list': [hero.id]
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Hero.objects.all().count(), 0)
