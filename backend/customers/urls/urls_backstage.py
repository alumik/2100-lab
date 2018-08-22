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
]
