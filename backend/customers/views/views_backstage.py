import re
import random
import time

from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse

from core.utils import get_page, get_backstage_page
from core.messages import ERROR, INFO
from customers.models import OrderLog


@permission_required('customers.view_orderlog')
def get_order_list(request):
    order_no = request.GET.get('order_no', '')
    course_codename = request.GET.get('course_codename', '')
    course_title = request.GET.get('course_title')
    customer_username = request.GET.get('customer_username')
    is_refunded = request.GET.get('is_refunded', '0')

    orders = OrderLog.objects.filter(
        order_no__contains=order_no,
        course__codename__contains=course_codename,
        course__title__contains=course_title,
        customer__username__contains=customer_username,
    ).order_by('-created_at')
    if is_refunded == '1':
        orders = orders.filter(refunded_at=None)
    elif is_refunded == '2':
        orders = orders.exclude(refunded_at=None)

    page = get_backstage_page(request, orders)
    page['order_no'] = order_no
    page['course_codename'] = course_codename
    page['course_title'] = course_title
    page['customer_username'] = customer_username
    page['is_refunded'] = is_refunded
    return JsonResponse(page, safe=False)
