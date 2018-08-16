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
        'personal-center/get-learning-logs/',
        views.personal_center_get_learning_logs,
        name='personal-center-get-learning-logs'
    ),
    path(
        'personal-center/get-order-logs/',
        views.personal_center_get_order_logs,
        name='personal-center-get-order-logs'
    ),
    path(
        'personal-center/change-username/',
        views.personal_center_change_username,
        name='personal-center-change-username'
    ),
    path(
        'auth/get-eula/',
        views.get_eula,
        name='get-eula'
    ),
    path(
        'auth/get-verification-code/',
        views.get_verification_code,
        name='get-verification-code'
    ),
    path(
        'auth/authenticate-customer/',
        views.authenticate_customer,
        name='authenticate-customer'
    ),
]
