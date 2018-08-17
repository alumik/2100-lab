import json
import pytz

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Course, Image, Comment, Hero
from customers.models import LearningLog, OrderLog


class MainPageTests(TestCase):
    def test_get_heroes(self):
        for index in range(1, 4):
            Hero.objects.create(
                image='fake/path/image' + str(index) + '.png',
                caption='c' + str(index)
            )

        response = self.client.get(reverse('api:courses:get-heroes'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'count': 3,
                'content': [
                    {
                        'image': 'fake/path/image1.png',
                        'caption': 'c1'
                    },
                    {
                        'image': 'fake/path/image2.png',
                        'caption': 'c2'
                    },
                    {
                        'image': 'fake/path/image3.png',
                        'caption': 'c3'
                    }
                ]
            }
        )

    def test_get_recent_courses(self):
        Course.objects.create(
            title='t1',
            description='d1',
            codename='c1'
        )
        Course.objects.create(
            title='t2',
            description='d2',
            codename='c2',
            price='200.00'
        )
        Course.objects.create(
            title='t3',
            description='d3',
            codename='c3'
        )
        Course.objects.create(
            title='t4',
            description='d4',
            codename='c4'
        )
        Course.objects.create(
            title='t5',
            description='d5',
            codename='c5',
            price='500.00'
        )

        response = self.client.get(reverse('api:courses:get-recent-courses'))
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['free_courses'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['free_courses'][0]['title'], 't4')
        self.assertEqual(response_json_data['free_courses'][0]['description'], 'd4')
        self.assertEqual(response_json_data['free_courses'][1]['thumbnail'], '')
        self.assertEqual(response_json_data['free_courses'][1]['title'], 't3')
        self.assertEqual(response_json_data['free_courses'][1]['description'], 'd3')
        self.assertEqual(response_json_data['free_courses'][2]['thumbnail'], '')
        self.assertEqual(response_json_data['free_courses'][2]['title'], 't1')
        self.assertEqual(response_json_data['free_courses'][2]['description'], 'd1')
        self.assertEqual(response_json_data['paid_courses'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['paid_courses'][0]['title'], 't5')
        self.assertEqual(response_json_data['paid_courses'][0]['description'], 'd5')
        self.assertEqual(response_json_data['paid_courses'][1]['thumbnail'], '')
        self.assertEqual(response_json_data['paid_courses'][1]['title'], 't2')
        self.assertEqual(response_json_data['paid_courses'][1]['description'], 'd2')


class CourseListTests(TestCase):
    def setUp(self):
        Course.objects.create(
            title='t1',
            description='d1',
            codename='c1'
        )
        Course.objects.create(
            title='t2',
            description='d2',
            codename='c2',
            price='200.00'
        )
        Course.objects.create(
            title='t3',
            description='d3',
            codename='c3'
        )
        Course.objects.create(
            title='t4',
            description='d4',
            codename='c4'
        )
        Course.objects.create(
            title='t5',
            description='d5',
            codename='c5',
            price='500.00'
        )

    def test_get_free_course_list(self):
        response = self.client.post(
            reverse('api:courses:get-course-list') + '?course_type=free&page=1',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 3)
        self.assertEqual(response_json_data['content'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['content'][0]['title'], 't4')
        self.assertEqual(response_json_data['content'][0]['description'], 'd4')

        response = self.client.post(
            reverse('api:courses:get-course-list') + '?course_type=free&page=3',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 3)
        self.assertEqual(response_json_data['content'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['content'][0]['title'], 't1')
        self.assertEqual(response_json_data['content'][0]['description'], 'd1')

    def test_get_paid_course_list(self):
        response = self.client.post(
            reverse('api:courses:get-course-list') + '?course_type=paid&page=1',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['content'][0]['title'], 't5')
        self.assertEqual(response_json_data['content'][0]['description'], 'd5')


class CourseDetailTests(TestCase):
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
            expire_duration=timezone.timedelta(days=1, hours=5)
        )
        Course.objects.create(
            title='t3',
            description='d3',
            codename='c3'
        )
        Course.objects.create(
            title='t4',
            description='d4',
            codename='c4',
            expire_duration=timezone.timedelta(days=3, hours=7)
        )

        LearningLog.objects.create(
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c1')
        )
        LearningLog.objects.create(
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c2'),
            expire_time=timezone.datetime(1997, 8, 17, tzinfo=pytz.UTC)
        )
        LearningLog.objects.create(
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c3')
        )

    def test_get_new_free_course_detail(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))
        course_id = Course.objects.get(codename='c4').id

        response = self.client.get(
            reverse('api:courses:get-customer-course-detail'),
            {'course_id': course_id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['course_id'], course_id)
        self.assertEqual(response_json_data['thumbnail'], '')
        self.assertEqual(response_json_data['title'], 't4')
        self.assertEqual(response_json_data['description'], 'd4')
        self.assertEqual(response_json_data['price'], '0.00')
        self.assertEqual(response_json_data['up_votes'], 0)
        self.assertEqual(response_json_data['expire_duration'], 'P3DT07H00M00S')
        self.assertIsNone(response_json_data['expire_time']),
        self.assertTrue(response_json_data['can_access'])

        self.client.logout()

    def test_get_old_free_course_detail_no_expire(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))
        course_id = Course.objects.get(codename='c3').id

        response = self.client.get(
            reverse('api:courses:get-customer-course-detail'),
            {'course_id': course_id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['course_id'], course_id)
        self.assertEqual(response_json_data['thumbnail'], '')
        self.assertEqual(response_json_data['title'], 't3')
        self.assertEqual(response_json_data['description'], 'd3')
        self.assertEqual(response_json_data['price'], '0.00')
        self.assertEqual(response_json_data['up_votes'], 0)
        self.assertEqual(response_json_data['expire_duration'], 'P0DT00H00M00S')
        self.assertIsNone(response_json_data['expire_time'])
        self.assertTrue(response_json_data['can_access'])

        self.client.logout()

    def test_get_old_free_course_detail_expire(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))
        course_id = Course.objects.get(codename='c2').id

        response = self.client.get(
            reverse('api:courses:get-customer-course-detail'),
            {'course_id': course_id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['course_id'], course_id)
        self.assertEqual(response_json_data['thumbnail'], '')
        self.assertEqual(response_json_data['title'], 't2')
        self.assertEqual(response_json_data['description'], 'd2')
        self.assertEqual(response_json_data['price'], '0.00')
        self.assertEqual(response_json_data['up_votes'], 0)
        self.assertEqual(response_json_data['expire_duration'], 'P1DT05H00M00S')
        self.assertEqual(response_json_data['expire_time'], '1997-08-17T00:00:00Z')
        self.assertTrue(response_json_data['can_access'])

        self.client.logout()

    def test_get_paid_course_detail_with_ref(self):
        OrderLog.objects.create(
            order_no='AA01',
            customer=get_user_model().objects.get(phone_number='13312345678'),
            course=Course.objects.get(codename='c1'),
            cash_spent=70,
            payment_method=1
        )
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))
        course_id = Course.objects.get(codename='c1').id

        response = self.client.get(
            reverse('api:courses:get-customer-course-detail'),
            {
                'course_id': course_id,
                'referer_id': '1234'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['referer_id'], '1234')
        self.assertTrue(json.loads(response.content)['can_access'])

        self.client.logout()

    def test_up_vote_course_logged_out(self):
        course_id = Course.objects.get(codename='c1').id

        response = self.client.get(
            reverse('api:courses:up-vote-course'),
            {'course_id': course_id}
        )
        self.assertEqual(response.status_code, 302)

    def test_up_vote_course_not_exists(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(
            reverse('api:courses:up-vote-course'),
            {'course_id': 10000}
        )
        self.assertEqual(response.status_code, 404)

    def test_up_vote_course_logged_in(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))
        course = Course.objects.get(codename='c1')
        self.assertEqual(course.up_votes.count(), 0)

        response = self.client.get(
            reverse('api:courses:up-vote-course'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(course.up_votes.count(), 1)

        response = self.client.get(
            reverse('api:courses:up-vote-course'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(course.up_votes.count(), 0)


class PlayPageTests(TestCase):
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
            reverse('api:courses:get-course-assets'),
            {'course_id': Course.objects.get(codename='c2').id}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Access denied.')

        response = self.client.get(
            reverse('api:courses:get-course-assets'),
            {'course_id': Course.objects.get(codename='c4').id}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Access denied.')

        self.client.logout()

    def test_play_module_access_granted(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(
            reverse('api:courses:get-course-assets'),
            {'course_id': Course.objects.get(codename='c1').id}
        )
        self.assertEqual(response.status_code, 403)

        course = Course.objects.get(codename='c3')
        response = self.client.get(
            reverse('api:courses:get-course-assets') + '?course_id=' + str(course.id)
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

        response = self.client.post(
            reverse('api:courses:get-course-comments')
            + '?course_id=' + str(Course.objects.get(codename='c1').id) + '&page=1',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
