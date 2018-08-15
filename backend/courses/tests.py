import json

from django.test import TestCase
from django.urls import reverse

from .models import Heroes, Course


class MainPageTests(TestCase):
    def test_get_heroes(self):
        Heroes.objects.create(
            image='fake/path/image1.png',
            caption='c1'
        )
        Heroes.objects.create(
            image='fake/path/image2.png',
            caption='c2'
        )
        Heroes.objects.create(
            image='fake/path/image3.png',
            caption='c3'
        )

        response = self.client.get(reverse('api:courses:get_heroes'))
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

        response = self.client.get(reverse('api:courses:get_recent_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'free_courses': [
                    {
                        'id': 4,
                        'thumbnail': '',
                        'title': 't4',
                        'description': 'd4'
                    },
                    {
                        'id': 3,
                        'thumbnail': '',
                        'title': 't3',
                        'description': 'd3'
                    },
                    {
                        'id': 1,
                        'thumbnail': '',
                        'title': 't1',
                        'description': 'd1'
                    }
                ],
                'paid_courses': [
                    {
                        'id': 5,
                        'thumbnail': '',
                        'title': 't5',
                        'description': 'd5'
                    },
                    {
                        'id': 2,
                        'thumbnail': '',
                        'title': 't2',
                        'description': 'd2'
                    }
                ]
            }
        )
