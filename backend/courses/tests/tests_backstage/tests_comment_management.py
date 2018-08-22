import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from courses.models import Course, Comment


class CommentListTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(phone_number='14412345678', password='123456')
        admin = get_user_model().objects.create_user(phone_number='13312345678', password='123456')
        permission = Permission.objects.get(codename='view_comment')
        admin_group = Group.objects.create(name='comment_admin')
        admin_group.permissions.add(permission)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()
        course = Course.objects.create(
            title='t1',
            description='d1',
            codename='SOFT1'
        )
        Comment.objects.create(
            user=user,
            course=course,
            content='1234'
        )
        Comment.objects.create(
            user=user,
            course=course,
            content='5678'
        )
        Comment.objects.create(
            user=user,
            course=course,
            content='90'
        ).delete()

    def test_comment_list_access_denied(self):
        self.client.login(phone_number='14412345678', password='123456')

        response = self.client.get(
            reverse('api:courses:backstage:get-comment-list'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_comment_list_no_filter(self):
        self.maxDiff = None
        self.client.login(phone_number='13312345678', password='123456')
        user = get_user_model().objects.get(phone_number='14412345678')
        comment = Comment.all_objects.get(content='90')

        response = self.client.get(
            reverse('api:courses:backstage:get-comment-list'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '',
                'count': 3,
                'page': 1,
                'num_pages': 3,
                'content': [
                    {
                        'comment_id': comment.id,
                        'created_at': response_json_data['content'][0]['created_at'],
                        'username': user.username,
                        'course_codename': 'SOFT1',
                        'course_title': 't1',
                        'content': '90',
                        'is_deleted': True
                    }
                ]
            }
        )

    def test_comment_list_not_deleted(self):
        self.maxDiff = None
        self.client.login(phone_number='13312345678', password='123456')
        user = get_user_model().objects.get(phone_number='14412345678')
        comment = Comment.all_objects.get(content='5678')

        response = self.client.get(
            reverse('api:courses:backstage:get-comment-list'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '1',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '1',
                'count': 2,
                'page': 1,
                'num_pages': 2,
                'content': [
                    {
                        'comment_id': comment.id,
                        'created_at': response_json_data['content'][0]['created_at'],
                        'username': user.username,
                        'course_codename': 'SOFT1',
                        'course_title': 't1',
                        'content': '5678',
                        'is_deleted': False
                    }
                ]
            }
        )

    def test_comment_list_deleted(self):
        self.maxDiff = None
        self.client.login(phone_number='13312345678', password='123456')
        user = get_user_model().objects.get(phone_number='14412345678')
        comment = Comment.all_objects.get(content='90')

        response = self.client.get(
            reverse('api:courses:backstage:get-comment-list'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '2',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '2',
                'count': 1,
                'page': 1,
                'num_pages': 1,
                'content': [
                    {
                        'comment_id': comment.id,
                        'created_at': response_json_data['content'][0]['created_at'],
                        'username': user.username,
                        'course_codename': 'SOFT1',
                        'course_title': 't1',
                        'content': '90',
                        'is_deleted': True
                    }
                ]
            }
        )

    def test_comment_detail(self):
        self.client.login(phone_number='13312345678', password='123456')
        comment = Comment.all_objects.get(content='1234')

        response = self.client.get(
            reverse('api:courses:backstage:get-comment-detail'),
            {'comment_id': comment.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'comment_id': comment.id,
                'created_at': response_json_data['created_at'],
                'username': comment.user.username,
                'course_codename': comment.course.codename,
                'course_title': comment.course.title,
                'is_deleted': comment.deleted_at is not None,
                'deleted_at': response_json_data['deleted_at'],
                'up_votes': comment.up_votes.count(),
                'down_votes': comment.down_votes.count(),
                'content': comment.content
            }
        )


class CommentOperationTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(phone_number='14412345678', password='123456')
        admin = get_user_model().objects.create_user(phone_number='13312345678', password='123456')
        admin_group = Group.objects.create(name='comment_admin')
        permission = Permission.objects.get(codename='view_comment')
        admin_group.permissions.add(permission)
        permission = Permission.objects.get(codename='add_comment')
        admin_group.permissions.add(permission)
        permission = Permission.objects.get(codename='delete_comment')
        admin_group.permissions.add(permission)
        admin_group.save()
        admin.groups.add(admin_group)
        admin.save()
        course = Course.objects.create(
            title='t1',
            description='d1',
            codename='SOFT1'
        )
        Comment.objects.create(
            user=user,
            course=course,
            content='1234'
        )

    def test_add_comment(self):
        self.client.login(phone_number='13312345678', password='123456')

        response = self.client.post(
            reverse('api:courses:backstage:add-comment'),
            {
                'course_codename': 'SOFT1',
                'comment_content': '12345678'
            }
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            reverse('api:courses:backstage:get-comment-list'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '0',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '0',
                'count': 2,
                'page': 1,
                'num_pages': 2,
                'content': [
                    {
                        'comment_id': response_json_data['content'][0]['comment_id'],
                        'created_at': response_json_data['content'][0]['created_at'],
                        'username': '13312345678',
                        'course_codename': 'SOFT1',
                        'course_title': 't1',
                        'content': '12345678',
                        'is_deleted': False
                    }
                ]
            }
        )

    def test_delete_comment(self):
        self.client.login(phone_number='13312345678', password='123456')
        comment = Comment.objects.get(content='1234')

        response = self.client.get(
            reverse('api:courses:backstage:get-comment-list'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '1',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 1)

        response = self.client.get(
            reverse('api:courses:backstage:delete-comment'),
            {'comment_id': comment.id}
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['message'], 'Object deleted.')

        response = self.client.get(
            reverse('api:courses:backstage:get-comment-list'),
            {
                'username': '',
                'course_codename': '',
                'course_title': '',
                'is_deleted': '1',
                'page': 1,
                'page_limit': 1
            }
        )
        self.assertEqual(response.status_code, 200)
        response_json_data = json.loads(response.content)
        self.assertEqual(response_json_data['count'], 0)
