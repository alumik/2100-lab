# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'customers'

urlpatterns = [
    path(
        'personal-center/get-customer-detail/',
        views.personal_center_get_customer_detail,
        name='personal-center-get-customer-detail'
    ),
    path(
        'personal-center/change-username/',
        views.personal_center_change_username,
        name='personal-center-change-username'
    ),
    path(
        'personal-center/get-learning-log/',
        views.personal_center_get_learning_log,
        name='personal-center-get-learning-log'
    ),
    path(
        'personal-center/get-order-log/',
        views.personal_center_get_order_log,
        name='personal-center-get-order-log'
    ),
]
