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
    path(
        'personal_center/learning_log/',
        views.personal_center_learning_log,
        name='personal_center_learning_log'
    ),
    path(
        'personal_center/order_log/',
        views.personal_center_order_log,
        name='personal_center_order_log'
    )
]
