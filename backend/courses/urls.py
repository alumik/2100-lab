# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('util/get-heroes/', views.get_heroes, name='get-heroes'),
    path('courses/get-recent-courses/', views.get_recent_courses, name='get-recent-courses'),
]
