import json

from django.test import TestCase
from django.urls import reverse

from courses.models import Course


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
            reverse('api:courses:forestage:get-course-list') + '?course_type=free&page=1',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 3)
        self.assertEqual(response_json_data['content'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['content'][0]['title'], 't4')
        self.assertEqual(response_json_data['content'][0]['description'], 'd4')

        response = self.client.post(
            reverse('api:courses:forestage:get-course-list') + '?course_type=free&page=3',
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
            reverse('api:courses:forestage:get-course-list') + '?course_type=paid&page=1',
            {'page_limit': 1}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 2)
        self.assertEqual(response_json_data['content'][0]['thumbnail'], '')
        self.assertEqual(response_json_data['content'][0]['title'], 't5')
        self.assertEqual(response_json_data['content'][0]['description'], 'd5')