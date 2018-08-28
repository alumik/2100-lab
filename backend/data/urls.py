# pylint: disable=C0103

from django.urls import path

from data import views

app_name = 'data'

urlpatterns = [
    path(
        'data-management/get-overall-data/',
        views.get_overall_data,
        name='get-overall-data'
    ),
    path(
        'data-management/get-data-by-time/',
        views.get_data_by_time,
        name='get-data-by-time'
    )
]
