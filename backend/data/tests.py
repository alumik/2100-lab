import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from courses.models import Course, CourseUpVotes


class DataTests(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            phone_number='15500000000',
            password='123456',
            is_staff=True,
            is_superuser=True
        )
        user_1 = get_user_model().objects.create_user(phone_number='10000000000')
        user_2 = get_user_model().objects.create_user(phone_number='20000000000')
        user_3 = get_user_model().objects.create_user(phone_number='30000000000')
        user_4 = get_user_model().objects.create_user(phone_number='40000000000')
        user_5 = get_user_model().objects.create_user(phone_number='50000000000')
        user_6 = get_user_model().objects.create_user(phone_number='60000000000')
        course_1 = Course.objects.create(
            title='t1',
            codename='c1',
            description='d1'
        )
        course_2 = Course.objects.create(
            title='t2',
            codename='c2',
            description='d2'
        )
        course_3 = Course.objects.create(
            title='t3',
            codename='c3',
            description='d3'
        )
        CourseUpVotes.objects.create(
            course=course_2,
            customer=user_1
        )
        CourseUpVotes.objects.create(
            course=course_2,
            customer=user_2
        )
        CourseUpVotes.objects.create(
            course=course_2,
            customer=user_3
        )
        CourseUpVotes.objects.create(
            course=course_3,
            customer=user_4
        )
        CourseUpVotes.objects.create(
            course=course_1,
            customer=user_5
        )
        CourseUpVotes.objects.create(
            course=course_1,
            customer=user_6
        )

    def test_overall_data(self):
        self.client.login(phone_number='15500000000', password='123456')

        response = self.client.get(
            reverse('api:data:get-overall-data'),
            {'days': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['customers_count'], 6)
        self.assertEqual(response_json_data['top_up_voted_courses'][0]['title'], 't2')
        self.assertEqual(response_json_data['top_up_voted_courses'][0]['up_votes'], 3)
