import json
import pytz

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from customers.models import LearningLog, OrderLog
from courses.models import Course


class CourseDetailTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(phone_number='13312345678')
        Course.objects.create(
            title='t1',
            description='d1',
            codename='c1',
            price='100.00',
            reward_percent='0.10'
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
            reverse('api:courses:forestage:get-course-detail'),
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
        self.assertTrue(response_json_data['can_access'])

        self.client.logout()

    def test_get_old_free_course_detail_no_expire(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))
        course_id = Course.objects.get(codename='c3').id

        response = self.client.get(
            reverse('api:courses:forestage:get-course-detail'),
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
            reverse('api:courses:forestage:get-course-detail'),
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
            reverse('api:courses:forestage:get-course-detail'),
            {
                'course_id': course_id,
                'referer_id': '1234'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session['referer_id'], '1234')
        self.assertEqual(json.loads(response.content)['reward_percent'], '0.10')
        self.assertTrue(json.loads(response.content)['can_access'])

        self.client.logout()

    def test_up_vote_course_logged_out(self):
        course_id = Course.objects.get(codename='c1').id

        response = self.client.get(
            reverse('api:courses:forestage:up-vote-course'),
            {'course_id': course_id}
        )
        self.assertEqual(response.status_code, 302)

    def test_up_vote_course_not_exists(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))

        response = self.client.get(
            reverse('api:courses:forestage:up-vote-course'),
            {'course_id': 10000}
        )
        self.assertEqual(response.status_code, 404)

    def test_up_vote_course_logged_in(self):
        self.client.force_login(get_user_model().objects.get(phone_number='13312345678'))
        course = Course.objects.get(codename='c1')
        self.assertEqual(course.up_votes.count(), 0)

        response = self.client.get(
            reverse('api:courses:forestage:up-vote-course'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(course.up_votes.count(), 1)

        response = self.client.get(
            reverse('api:courses:forestage:up-vote-course'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(course.up_votes.count(), 0)


class BuyCourseTest(TestCase):
    def test_buy_course(self):
        user_0 = get_user_model().objects.create_user(phone_number='00000000000')
        user_1 = get_user_model().objects.create_user(phone_number='00000000001')
        user_2 = get_user_model().objects.create_user(phone_number='00000000002')
        user_1.reward_coin = 30
        user_2.reward_coin = 70
        user_1.save()
        user_2.save()
        course = Course.objects.create(
            codename='c1',
            title='t1',
            description='d1',
            price=50,
            reward_percent=0.5
        )

        self.client.force_login(user_1)
        self.client.get(
            reverse('api:courses:forestage:get-course-detail'),
            {
                'course_id': course.id,
                'referer_id': user_0.id
            }
        )
        response = self.client.post(
            reverse('api:courses:forestage:buy-course'),
            {'course_id': course.id}
        )
        user_0 = get_user_model().objects.get(phone_number='00000000000')
        user_1 = get_user_model().objects.get(phone_number='00000000001')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(user_1.reward_coin), 0)
        self.assertEqual(int(user_0.reward_coin), 25)
        self.assertEqual(int(OrderLog.objects.get(customer__phone_number='00000000001').cash_spent), 20)
        self.client.logout()

        self.client.force_login(user_2)
        self.client.get(
            reverse('api:courses:forestage:get-course-detail'),
            {
                'course_id': course.id,
                'referer_id': user_0.id
            }
        )
        response = self.client.post(
            reverse('api:courses:forestage:buy-course'),
            {'course_id': course.id}
        )
        user_0 = get_user_model().objects.get(phone_number='00000000000')
        user_2 = get_user_model().objects.get(phone_number='00000000002')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(user_2.reward_coin), 20)
        self.assertEqual(int(user_0.reward_coin), 50)
        self.assertEqual(int(OrderLog.objects.get(customer__phone_number='00000000002').cash_spent), 0)
        self.client.logout()
