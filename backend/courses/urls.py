# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path(
        'util/get-heroes/',
        views.get_heroes,
        name='get-heroes'
    ),
    path(
        'courses/get-recent-courses/',
        views.get_recent_courses,
        name='get-recent-courses'
    ),
    path(
        'courses/get-course-list/',
        views.get_course_list,
        name='get-course-list'
    ),
    path(
        'courses/get-customer-course-detail/',
        views.get_customer_course_detail,
        name='get-customer-course-detail'
    ),
    path(
        'courses/up-vote-course/',
        views.up_vote_course,
        name='up-vote-course'
    ),
    path(
        'course/get-course-assets/',
        views.get_course_assets,
        name='get-course-assets'
    ),
]
