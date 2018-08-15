# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path(
        'util/get_heroes/',
        views.get_heroes,
        name='get_heroes'
    ),
    path(
        'courses/recent_courses/',
        views.get_recent_courses,
        name='get_recent_courses'
    ),
]
