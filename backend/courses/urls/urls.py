# pylint: disable=C0103

from django.urls import path, include

app_name = 'courses'

urlpatterns = [
    path(
        'forestage/',
        include('courses.urls.urls_forestage', namespace='forestage')
    ),
    path(
        'backstage/',
        include('courses.urls.urls_backstage', namespace='backstage')
    )
]
