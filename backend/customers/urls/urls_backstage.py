# pylint: disable=C0103, E0401

from django.urls import path

from customers.views import views_backstage

app_name = 'customers'

urlpatterns = [
    path(
        'order-management/get-order-list/',
        views_backstage.get_order_list,
        name='get-order-list'
    ),
    path(
        'order-management/get-order-detail/',
        views_backstage.get_order_detail,
        name='get-order-detail'
    ),
    path(
        'order-management/order-refund/',
        views_backstage.order_refund,
        name='order-refund'
    ),
    path(
        'customer-management/get-customer-list/',
        views_backstage.get_customer_list,
        name='get-customer-list'
    ),
    path(
        'customer-management/get-customer-detail/',
        views_backstage.get_customer_detail,
        name='get-customer-detail'
    ),
    path(
        'customer-management/get-customer-order-list/',
        views_backstage.get_customer_order_list,
        name='get-customer-order-list'
    ),
    path(
        'customer-management/get-customer-learning-log-list/',
        views_backstage.get_customer_learning_log_list,
        name='get-customer-learning-log-list'
    ),
    path(
        'customer-management/toggle-vip/',
        views_backstage.toggle_vip,
        name='toggle-vip'
    ),
    path(
        'customer-management/toggle-banned/',
        views_backstage.toggle_banned,
        name='toggle-banned'
    ),
    path(
        'customer-management/delete-customer/',
        views_backstage.delete_customer,
        name='delete-customer'
    ),
]
