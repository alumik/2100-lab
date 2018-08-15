# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('util/get-heroes/', views.get_heroes, name='get-heroes'),
    path('courses/get-recent-courses/', views.get_recent_courses, name='get-recent-courses'),
    path('courses/get-free-course-list/', views.get_free_course_list, name='get-free-course-list'),
    path('courses/get-paid-course-list/', views.get_paid_course_list, name='get-paid-course-list'),
    path('courses/get-course-detail/', views.get_course_detail, name='get-course-detail'),
]
