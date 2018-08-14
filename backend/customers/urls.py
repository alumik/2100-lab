# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'customers'

urlpatterns = [
    path(
        'personal_center/main_page/',
        views.personal_center_main_page,
        name='personal_center_main_page'
    ),
    path(
        'personal_center/change_username/',
        views.personal_center_change_username,
        name='personal_center_change_username'
    ),
]