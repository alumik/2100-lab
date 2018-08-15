import json

from django.test import TestCase
from django.urls import reverse

from .models import Heroes


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
