# pylint: disable=C0103, E0401

from django.urls import path

from customers.views import views_forestage

app_name = 'customers'

urlpatterns = [
    path(
        'personal-center/get-customer-detail/',
        views_forestage.get_customer_detail,
        name='get-customer-detail'
    ),
    path(
        'personal-center/get-reward-coin/',
        views_forestage.get_reward_coin,
        name='get-reward-coin'
    ),
    path(
        'personal-center/get-learning-logs/',
        views_forestage.get_learning_logs,
        name='get-learning-logs'
    ),
    path(
        'personal-center/get-order-logs/',
        views_forestage.get_order_logs,
        name='get-order-logs'
    ),
    path(
        'personal-center/change-username/',
        views_forestage.change_username,
        name='change-username'
    ),
    path(
        'auth/get-eula/',
        views_forestage.get_eula,
        name='get-eula'
    ),
    path(
        'auth/get-generate-time/',
        views_forestage.get_generate_time,
        name='get-generate-time'
    ),
    path(
        'auth/get-verification-code/',
        views_forestage.get_verification_code,
        name='get-verification-code'
    ),
    path(
        'auth/authenticate-customer/',
        views_forestage.authenticate_customer,
        name='authenticate-customer'
    ),
]
