import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from customers.models import OrderLog
from courses.models import Course, Image, Comment


class CoursePlayTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13312345678')
        Course.objects.create(
            title='t1',
            description='d1',
            codename='c1',
            price='100.00'
        )
        Course.objects.create(
            title='t2',
            description='d2',
            codename='c2',
            price='100.00'
        )
        Course.objects.create(
            title='t3',
            description='d3',
            codename='c3',
            price='100.00'
        )
        Course.objects.create(
            title='t4',
            description='d4',
            codename='c4',
            price='100.00'
        )
        OrderLog.objects.create(
            order_no='AA01',
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c3'),
            cash_spent=70,
            payment_method=1
        )
        OrderLog.objects.create(
            order_no='AA02',
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c4'),
            cash_spent=50,
            reward_spent=50,
            payment_method=2,
            refunded_at=timezone.now()
        )
        Image.objects.create(
            course=Course.objects.get(codename='c3'),
            image_path='fake/path/to/img1.png',
            load_time=200,
        )
        Image.objects.create(
            course=Course.objects.get(codename='c3'),
            image_path='fake/path/to/img2.png',
            load_time=100,
        )

    def test_play_module_access_denied(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(
            reverse('api:courses:forestage:get-course-assets'),
            {'course_id': Course.objects.get(codename='c2').id}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Access denied.')

        response = self.client.get(
            reverse('api:courses:forestage:get-course-assets'),
            {'course_id': Course.objects.get(codename='c4').id}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Access denied.')

        self.client.logout()

    def test_play_module_access_granted(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(
            reverse('api:courses:forestage:get-course-assets'),
            {'course_id': Course.objects.get(codename='c1').id}
        )
        self.assertEqual(response.status_code, 403)

        course = Course.objects.get(codename='c3')
        response = self.client.get(
            reverse('api:courses:forestage:get-course-assets'),
            {'course_id': str(course.id)}
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'course_id': course.id,
                'title': course.title,
                'description': course.description,
                'audio': '',
                'images': [
                    {
                        'image_path': 'fake/path/to/img2.png',
                        'load_time': 100
                    },
                    {
                        'image_path': 'fake/path/to/img1.png',
                        'load_time': 200
                    },
                ],
                'progress': 0
            }
        )


class CommentTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13312345678')
        get_user_model().objects.create_user(phone_number='14412345678')
        Course.objects.create(
            title='t1',
            description='d1',
            codename='c1'
        )
        Comment.objects.create(
            course=Course.objects.get(codename='c1'),
            user=get_user_model().objects.get(phone_number='13312345678'),
            content='123456'
        )
        Comment.objects.create(
            course=Course.objects.get(codename='c1'),
            user=get_user_model().objects.get(phone_number='14412345678'),
            content='123456'
        )

    def test_get_comments(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(
            reverse('api:courses:forestage:get-course-comments'),
            {
                'course_id': Course.objects.get(codename='c1').id,
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)