from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import LearningLog, OrderLog


@login_required
def personal_center_get_customer_detail(request):
    user = request.user
    return JsonResponse(request.user.as_brief_dict())


@login_required
def personal_center_change_username(request):
    user = request.user
    username = request.POST.get('username')
    try:
        get_user_model().objects.get(username=username)
        return JsonResponse({'message': 'This username is already taken.'}, status=403)
    except get_user_model().DoesNotExist:
        user.username = username
        user.save()
        return JsonResponse({'username': username})


@login_required
def personal_center_get_learning_log(request):
    learning_log_object_list = LearningLog.objects.filter(customer=request.user).order_by('-created_at')
    count = learning_log_object_list.count()

    page = request.GET.get('page', request.POST['page'])
    paginator = Paginator(learning_log_object_list, request.POST['page_limit'])

    try:
        learning_log_objects = paginator.page(page)
    except PageNotAnInteger:
        learning_log_objects = paginator.page(request.POST['page'])
    except EmptyPage:
        learning_log_objects = paginator.page(paginator.num_pages)

    learning_log_list = list(
        map(lambda learning_log_object: learning_log_object.as_brief_dict(), list(learning_log_objects))
    )
    return JsonResponse(
        {
            'count': count,
            'content': learning_log_list
        },
        safe=False
    )


@login_required
def personal_center_get_order_log(request):
    order_log_object_list = OrderLog.objects.filter(customer=request.user).order_by('-created_at')
    count = order_log_object_list.count()

    page = request.GET.get('page', request.POST['page'])
    paginator = Paginator(order_log_object_list, request.POST['page_limit'])

    try:
        order_log_objects = paginator.page(page)
    except PageNotAnInteger:
        order_log_objects = paginator.page(request.POST['page'])
    except EmptyPage:
        order_log_objects = paginator.page(paginator.num_pages)

    order_log_list = list(
        map(lambda order_log_object: order_log_object.as_brief_dict(), list(order_log_objects))
    )
    return JsonResponse(
        {
            'count': count,
            'content': order_log_list
        },
        safe=False
    )
