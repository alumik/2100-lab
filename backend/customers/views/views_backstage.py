"""用户模块后台功能"""

import time

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.utils import timezone

from admins.models import AdminLog
from core.constants import ERROR, INFO, ACTION_TYPE
from core.utils import get_backstage_page, get_brief_page
from customers.models import OrderLog, LearningLog
from customers.utils import get_customer_page


@permission_required('customers.view_orderlog')
def get_order_list(request):
    """获取订单列表"""

    order_no = request.GET.get('order_no', '')
    course_codename = request.GET.get('course_codename', '')
    course_title = request.GET.get('course_title', '')
    customer_username = request.GET.get('customer_username', '')
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


@permission_required('customers.view_orderlog')
def get_order_detail(request):
    """获取订单详情"""

    order_id = request.GET.get('order_id')

    try:
        order = OrderLog.objects.get(id=order_id)
    except OrderLog.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    return JsonResponse(
        {
            'order_id': order.id,
            'order_no': order.order_no,
            'course_codename': order.course.codename,
            'course_title': order.course.title,
            'customer_username': order.customer.username,
            'money': order.cash_spent + order.reward_spent,
            'is_refunded': order.refunded_at is not None,
            'created_at': order.created_at,
            'refunded_at': order.refunded_at
        }
    )


@permission_required('customers.change_orderlog')
def order_refund(request):
    """订单退款"""

    order_id = request.POST.get('order_id')

    try:
        order = OrderLog.objects.get(id=order_id)
    except OrderLog.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    # payment_method = order.payment_method
    # cash_spent = order.cash_spent
    reward_spent = order.reward_spent
    customer = order.customer
    customer.reward_coin += reward_spent
    customer.save()
    order.refunded_at = timezone.now()

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['refund_order'],
        new_data=customer.id,
        object_id=order_id
    )
    order.save()

    return JsonResponse({'message': INFO['success']})


@permission_required('core.view_customuser')
def get_customer_list(request):
    """获取用户列表"""

    customer_id = request.GET.get('customer_id', '')
    username = request.GET.get('username', '')
    phone_number = request.GET.get('phone_number', '')
    is_vip = request.GET.get('is_vip', '0')
    is_banned = request.GET.get('is_banned', '0')

    customers = get_user_model().objects.filter(
        username__contains=username,
        phone_number__contains=phone_number,
        is_staff=False
    ).order_by('-updated_at')

    if customer_id != '':
        customers = customers.filter(id=int(customer_id))
    if is_vip == '1':
        customers = customers.filter(is_vip=False)
    elif is_vip == '2':
        customers = customers.filter(is_vip=True)
    if is_banned == '1':
        customers = customers.filter(is_banned=False)
    elif is_banned == '2':
        customers = customers.filter(is_banned=True)

    page = get_customer_page(request, customers)
    page['customer_id'] = customer_id
    page['username'] = username
    page['phone_number'] = phone_number
    page['is_vip'] = is_vip
    page['is_banned'] = is_banned
    return JsonResponse(page, safe=False)


@permission_required('core.view_customuser')
def get_customer_detail(request):
    """获取用户详情"""

    customer_id = request.GET.get('customer_id')

    try:
        customer = get_user_model().objects.get(id=customer_id, is_staff=False)
    except OrderLog.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    json_data = {
        'customer_info': {
            'avatar': str(customer.avatar),
            'user_id': customer.id,
            'username': customer.username,
            'phone_number': customer.phone_number,
            'reward_coin': customer.reward_coin,
            'is_vip': customer.is_vip,
            'is_banned': customer.is_banned,
            'date_joined': customer.date_joined,
            'updated_at': customer.updated_at
        },
        'recent_orders': [],
        'recent_learning_logs': []
    }

    recent_orders = OrderLog.objects.filter(
        customer=customer
    ).order_by('-created_at')[:5]
    recent_learning_logs = LearningLog.objects.filter(
        customer=customer
    ).order_by('-latest_learn')[:5]

    for recent_order in recent_orders:
        json_data['recent_orders'].append(recent_order.as_brief_dict())

    for recent_learning_log in recent_learning_logs:
        item = recent_learning_log.as_brief_dict()
        if recent_learning_log.expire_time is not None:
            if recent_learning_log.expire_time < timezone.now():
                item['is_burnt'] = True
        json_data['recent_learning_logs'].append(item)

    return JsonResponse(json_data)


@permission_required('core.view_customuser')
def get_customer_order_list(request):
    """获取用户订单列表"""

    customer_id = request.GET.get('customer_id')

    try:
        customer = get_user_model().objects.get(id=customer_id, is_staff=False)
    except OrderLog.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    orders = OrderLog.objects.filter(customer=customer).order_by('-created_at')
    return get_brief_page(request, orders)


@permission_required('core.view_customuser')
def get_customer_learning_log_list(request):
    """获取用户学习记录列表"""

    customer_id = request.GET.get('customer_id')

    try:
        customer = get_user_model().objects.get(id=customer_id, is_staff=False)
    except OrderLog.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    learning_logs = LearningLog.objects.filter(
        customer=customer
    ).order_by('-latest_learn')
    return get_brief_page(request, learning_logs)


@permission_required('core.change_customuser')
def toggle_vip(request):
    """切换认证用户状态"""

    customer_id = request.POST.get('customer_id')

    try:
        customer = get_user_model().objects.get(id=customer_id, is_staff=False)
    except OrderLog.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    customer.is_vip = not customer.is_vip
    customer.save()

    if customer.is_vip:
        AdminLog.objects.create(
            admin_user=request.user,
            action_type=ACTION_TYPE['set_vip_true'],
            object_id=customer_id
        )
    else:
        AdminLog.objects.create(
            admin_user=request.user,
            action_type=ACTION_TYPE['set_vip_false'],
            object_id=customer_id
        )
    return JsonResponse({'is_vip': customer.is_vip})


@permission_required('core.change_customuser')
def toggle_banned(request):
    """切换用户经验状态"""

    customer_id = request.POST.get('customer_id')

    try:
        customer = get_user_model().objects.get(id=customer_id, is_staff=False)
    except OrderLog.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    customer.is_banned = not customer.is_banned
    customer.save()

    if customer.is_banned:
        AdminLog.objects.create(
            admin_user=request.user,
            action_type=ACTION_TYPE['ban_customer_true'],
            object_id=customer_id
        )
    else:
        AdminLog.objects.create(
            admin_user=request.user,
            action_type=ACTION_TYPE['ban_customer_false'],
            object_id=customer_id
        )
    return JsonResponse({'is_banned': customer.is_banned})


@permission_required('core.delete_customuser')
def delete_customer(request):
    """删除用户"""

    customer_id = request.POST.get('customer_id')

    try:
        customer = get_user_model().objects.get(id=customer_id, is_staff=False)
    except OrderLog.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    delete_str = '_deleted_' + str(int(round(time.time() * 1000)))
    customer.phone_number += delete_str
    customer.username += delete_str

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['delete_customer'],
        object_id=customer_id
    )
    customer.delete()
    return JsonResponse({'message': INFO['object_deleted']})
