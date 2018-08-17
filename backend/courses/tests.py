import json
import pytz

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Course, Image, Comment
from customers.models import LearningLog, OrderLog
from core.utils import create_test_customers, create_test_heroes, create_test_courses


class MainPageTests(TestCase):
    def test_get_heroes(self):
        create_test_heroes(3)

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
        create_test_courses(5)
        _course = Course.objects.get(codename='c2')
        _course.price = '200.00'
        _course.save()
        _course = Course.objects.get(codename='c5')
        _course.price = '500.00'
        _course.save()

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
        create_test_courses(5)
        _course = Course.objects.get(codename='c2')
        _course.price = '200.00'
        _course.save()
        _course = Course.objects.get(codename='c5')
        _course.price = '500.00'
        _course.save()

    def test_get_free_course_list(self):
        response = self.client.post(
            reverse('api:courses:get-course-list'),
            {
                'course_type': Course.TYPE_FREE,
                'page_limit': 1,
                'page': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 3)
        self.assertEqual(response_json_data['content'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['content'][0]['title'], 't4')
        self.assertEqual(response_json_data['content'][0]['description'], 'd4')

        response = self.client.post(
            reverse('api:courses:get-course-list'),
            {
                'course_type': Course.TYPE_FREE,
                'page_limit': 1,
                'page': 3
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 3)
        self.assertEqual(response_json_data['content'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['content'][0]['title'], 't1')
        self.assertEqual(response_json_data['content'][0]['description'], 'd1')

    def test_get_paid_course_list(self):
        response = self.client.post(
            reverse('api:courses:get-course-list'),
            {
                'course_type': Course.TYPE_PAID,
                'page_limit': 1,
                'page': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['content'][0]['title'], 't5')
        self.assertEqual(response_json_data['content'][0]['description'], 'd5')


class CourseDetailTests(TestCase):
    def setUp(self):
        create_test_customers(1)
        create_test_courses(4)
        _course = Course.objects.get(codename='c1')
        _course.price = '100.00'
        _course.save()
        _course = Course.objects.get(codename='c2')
        _course.expire_duration = timezone.timedelta(days=1, hours=5)
        _course.save()
        _course = Course.objects.get(codename='c4')
        _course.expire_duration = timezone.timedelta(days=3, hours=7)
        _course.save()

        LearningLog.objects.create(
            customer=get_user_model().objects.get(phone_number='00000000001'),
            course=Course.objects.get(codename='c1')
        )
        LearningLog.objects.create(
            customer=get_user_model().objects.get(phone_number='00000000001'),
            course=Course.objects.get(codename='c2'),
            expire_time=timezone.datetime(1997, 8, 17, tzinfo=pytz.UTC)
        )
        LearningLog.objects.create(
            customer=get_user_model().objects.get(phone_number='00000000001'),
            course=Course.objects.get(codename='c3')
        )

    def test_get_new_free_course_detail(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
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
        self.assertIsNone(response_json_data['expire_time'])

        self.client.logout()

    def test_get_old_free_course_detail_no_expire(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
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

        self.client.logout()

    def test_get_old_free_course_detail_expire(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
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

        self.client.logout()

    def test_get_paid_course_detail_with_ref(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
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

        self.client.logout()

    def test_up_vote_course_logged_out(self):
        course_id = Course.objects.get(codename='c1').id

        response = self.client.post(
            reverse('api:courses:up-vote-course'),
            {'course_id': course_id}
        )
        self.assertEqual(response.status_code, 302)

    def test_up_vote_course_not_exists(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))

        response = self.client.post(
            reverse('api:courses:up-vote-course'),
            {'course_id': 10000}
        )
        self.assertEqual(response.status_code, 404)

    def test_up_vote_course_logged_in(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))
        course = Course.objects.get(codename='c1')
        self.assertEqual(course.up_votes.count(), 0)

        response = self.client.post(
            reverse('api:courses:up-vote-course'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(course.up_votes.count(), 1)

        response = self.client.post(
            reverse('api:courses:up-vote-course'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(course.up_votes.count(), 0)


class PlayPageTests(TestCase):
    def setUp(self):
        create_test_customers(1)
        create_test_courses(4)
        _course = Course.objects.get(codename='c2')
        _course.price = '100.00'
        _course.save()
        _course = Course.objects.get(codename='c3')
        _course.price = '100.00'
        _course.save()
        _course = Course.objects.get(codename='c4')
        _course.price = '100.00'
        _course.save()
        OrderLog.objects.create(
            order_no='AA01',
            customer=get_user_model().objects.get(phone_number='00000000001'),
            course=Course.objects.get(codename='c3'),
            cash_spent=70,
            payment_method=1
        )
        OrderLog.objects.create(
            order_no='AA02',
            customer=get_user_model().objects.get(phone_number='00000000001'),
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
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))

        response = self.client.post(
            reverse('api:courses:get-course-assets'),
            {'course_id': Course.objects.get(codename='c2').id}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Access denied.')

        response = self.client.post(
            reverse('api:courses:get-course-assets'),
            {'course_id': Course.objects.get(codename='c4').id}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.content)['message'], 'Access denied.')

        self.client.logout()

    def test_play_module_access_granted(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))

        response = self.client.post(
            reverse('api:courses:get-course-assets'),
            {'course_id': Course.objects.get(codename='c1').id}
        )
        self.assertEqual(response.status_code, 200)

        course = Course.objects.get(codename='c3')
        response = self.client.post(
            reverse('api:courses:get-course-assets'),
            {'course_id': course.id}
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
                ]
            }
        )


class CommentTests(TestCase):
    def setUp(self):
        create_test_customers(2)
        create_test_courses(1)
        Comment.objects.create(
            course=Course.objects.get(codename='c1'),
            user=get_user_model().objects.get(phone_number='00000000001'),
            content='123456'
        )
        Comment.objects.create(
            course=Course.objects.get(codename='c1'),
            user=get_user_model().objects.get(phone_number='00000000002'),
            content='123456'
        )

    def test_get_comments(self):
        self.client.force_login(get_user_model().objects.get(phone_number='00000000001'))

        response = self.client.post(
            reverse('api:courses:get-course-comments'),
            {
                'course_id': Course.objects.get(codename='c1').id,
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)

