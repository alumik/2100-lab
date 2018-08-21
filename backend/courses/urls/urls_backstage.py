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
        'comment-management/get-comment-list/',
        views_backstage.get_comment_list,
        name='get-comment-list'
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
