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
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'course_id': course.id,
                'title': course.title,
                'description': course.description,
                'audio': '',
                'images': [
                    {
                        'image_id': response_json_data['images'][0]['image_id'],
                        'image_path': 'fake/path/to/img2.png',
                        'load_time': 100
                    },
                    {
                        'image_id': response_json_data['images'][1]['image_id'],
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

    def test_add_comments_not_allowed(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))
        course = Course.objects.create(
            title='course_cannot_comment',
            description='course_cannot_comment',
            codename='course_cannot_comment',
            can_comment=False
        )

        response = self.client.post(
            reverse('api:courses:forestage:add-comment'),
            {
                'course_id': course.id,
                'content': 'Test comment.'
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_add_comment_and_reply(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))
        course = Course.objects.create(
            title='course_comment_and_reply',
            description='course_comment_and_reply',
            codename='course_comment_and_reply'
        )

        response = self.client.post(
            reverse('api:courses:forestage:add-comment'),
            {
                'course_id': course.id,
                'content': 'Test comment.'
            }
        )
        self.assertEqual(response.status_code, 200)
        reply_to_id = int(json.loads(response.content)['comment_id'])

        response = self.client.post(
            reverse('api:courses:forestage:add-comment'),
            {
                'course_id': course.id,
                'reply_to_id': reply_to_id,
                'content': 'Test reply.'
            }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('api:courses:forestage:get-course-comments'),
            {
                'course_id': course.id,
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 1)
        self.assertEqual(response_json_data['content'][0]['reply_count'], 1)
        self.assertEqual(response_json_data['content'][0]['replies'][0]['content'], 'Test reply.')
