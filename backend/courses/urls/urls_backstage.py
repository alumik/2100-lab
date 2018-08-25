# pylint: disable=C0103, E0401

from django.urls import path

from courses.views import views_backstage

app_name = 'courses'

urlpatterns = [
    path(
        'course-management/get-course-list/',
        views_backstage.get_course_list,
        name='get-course-list'
    ),
    path(
        'course-management/get-course-detail/',
        views_backstage.get_course_detail,
        name='get-course-detail'
    ),
    path(
        'course-management/delete-course/',
        views_backstage.delete_course,
        name='delete-course'
    ),
    path(
        'course-management/add-course/',
        views_backstage.add_course,
        name='add-course'
    ),
    path(
        'course-management/delete-course-images/',
        views_backstage.delete_course_images,
        name='delete-course-images'
    ),
    path(
        'course-management/add-hero/',
        views_backstage.add_hero,
        name='add-hero'
    ),
    path(
        'course-management/delete-hero/',
        views_backstage.delete_hero,
        name='delete-hero'
    ),
    path(
        'comment-management/get-comment-list/',
        views_backstage.get_comment_list,
        name='get-comment-list'
    ),
    path(
        'comment-management/get-comment-detail/',
        views_backstage.get_comment_detail,
        name='get-comment-detail'
    ),
    path(
        'comment-management/add-comment/',
        views_backstage.add_comment,
        name='add-comment'
    ),
    path(
        'comment-management/delete-comment/',
        views_backstage.delete_comment,
        name='delete-comment'
    ),
]
