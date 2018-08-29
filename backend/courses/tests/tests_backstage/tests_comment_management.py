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
        get_user_model().objects.create_user(
            phone_number='13312345678',
            password='123456',
            is_staff=True,
            is_superuser=True
        )
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

    def test_add_comment_not_allowed(self):
        self.client.login(phone_number='13312345678', password='123456')
        user = get_user_model().objects.get(phone_number='13312345678')
        course = Course.objects.create(
            title='t2',
            description='d2',
            codename='SOFT2',
            can_comment=False
        )
        Comment.objects.create(
            user=user,
            course=course,
            content='reply_to'
        )
        reply_to = Comment.objects.get(content='reply_to')
        response = self.client.post(
            reverse('api:courses:backstage:add-comment'),
            {
                'reply_to_id': reply_to.id,
                'comment_content': '12345678'
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_add_comment(self):
        self.client.login(phone_number='13312345678', password='123456')
        reply_to = Comment.objects.get(content='5678')

        response = self.client.post(
            reverse('api:courses:backstage:add-comment'),
            {
                'reply_to_id': reply_to.id,
                'comment_content': 'This is a reply.'
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
                'count': 3,
                'page': 1,
                'num_pages': 3,
                'content': [
                    {
                        'comment_id': response_json_data['content'][0]['comment_id'],
                        'created_at': response_json_data['content'][0]['created_at'],
                        'username': '13312345678',
                        'course_codename': 'SOFT1',
                        'course_title': 't1',
                        'content': 'This is a reply.',
                        'is_deleted': False
                    }
                ]
            }
        )
        self.assertEqual(Comment.objects.filter(parent=reply_to).count(), 1)

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
        self.assertEqual(response_json_data['count'], 2)

        response = self.client.post(
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
        self.assertEqual(response_json_data['count'], 1)

    def test_reply_to_reply(self):
        self.client.login(phone_number='13312345678', password='123456')
        user = get_user_model().objects.get(phone_number='13312345678')
        course = Course.objects.create(
            title='RTR',
            description='RTR',
            codename='RTR',
        )
        comment = Comment.objects.create(
            user=user,
            course=course,
            content='Comment'
        )
        reply = Comment.objects.create(
            user=user,
            course=course,
            content='Reply',
            parent=comment
        )

        response = self.client.post(
            reverse('api:courses:backstage:add-comment'),
            {
                'reply_to_id': reply.id,
                'comment_content': 'RTR'
            }
        )

        self.assertEqual(Comment.objects.filter(parent=comment).count(), 2)

        response = self.client.get(
            reverse('api:courses:forestage:get-course-comments'),
            {'course_id': course.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['count'], 1)
