from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.utils import timezone

from core.utils import get_backstage_page
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


@permission_required('customers.view_orderlog')
def get_order_detail(request):
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
    order.save()

    return JsonResponse({'message': INFO['success']})
