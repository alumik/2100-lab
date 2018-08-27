"""用户模块前台函数"""

import random
import re
import time

from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Comment out the following line to prevent sms being sent by CI server.
# from qcloudsms_py.httpclient import HTTPError

from core.constants import ERROR, INFO
from core.utils import get_page
from customers.models import LearningLog, OrderLog

# Comment out the following line to prevent sms being sent by CI server.
# from customers.utils import tencent_cloud_message


def get_verification_code(request):
    """获取短信验证码

    注：发送短信部分在测试时会被注释掉以防止测试时发送错误短信。
    """

    phone_number = request.POST.get('phone_number')
    match = re.search(r'^1\d{10}$', phone_number)
    if match:
        verification_code = str(random.randint(0, 999999)).zfill(6)

        # Comment out the following lines to prevent sms being sent by CI server.
        # try:
        #     tencent_cloud_message(phone_number, verification_code)
        # except (HTTPError, Exception):
        #     return JsonResponse(
        #         {'message': ERROR['message_send_failed']},
        #         status=500
        #     )

        request.session['prev_phone_number'] = phone_number
        request.session['verification_code'] = verification_code
        request.session['generate_time'] = round(time.time())
        try:
            get_user_model().objects.get(phone_number=phone_number)
            new_customer = False
        except get_user_model().DoesNotExist:
            new_customer = True
        return JsonResponse(
            {
                # debug only
                'verification_code': verification_code,
                'is_new_customer': new_customer
            }
        )
    return JsonResponse({'message': ERROR['invalid_phone_number']}, status=400)


def get_generate_time(request):
    """获取上一个短信验证码生成时间"""

    json_data = {'generate_time': ''}
    if 'generate_time' in request.session:
        json_data['generate_time'] = request.session['generate_time']
    return JsonResponse(json_data)


def authenticate_customer(request):
    """认证用户"""

    phone_number = request.POST.get('phone_number')
    verification_code = request.POST.get('verification_code')

    if phone_number != request.session['prev_phone_number']:
        return JsonResponse(
            {'message': ERROR['different_phone_number']},
            status=400
        )

    if verification_code != request.session['verification_code']:
        return JsonResponse(
            {'message': ERROR['invalid_verification_code']},
            status=400
        )

    try:
        user = get_user_model().objects.get(phone_number=phone_number)
        new_customer = False
    except get_user_model().DoesNotExist:
        user = get_user_model().objects.create_user(phone_number=phone_number)
        new_customer = True
    login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
    del request.session['verification_code']

    return JsonResponse(
        {
            'is_new_customer': new_customer,
            'customer_id': user.id,
            'username': user.username,
            'avatar': str(user.avatar)
        }
    )


def get_eula(request):
    """获取用户许可协议"""

    return JsonResponse({'content': 'Test EULA.'})


@login_required
def change_username(request):
    """修改用户名"""

    user = request.user
    username = request.POST.get('username')
    try:
        get_user_model().objects.get(username=username)
        return JsonResponse(
            {'message': ERROR['username_already_taken']},
            status=400
        )
    except get_user_model().DoesNotExist:
        if re.match(r'^.*_deleted_.*$', username):
            return JsonResponse(
                {'message': ERROR['invalid_username']},
                status=400
            )
        user.username = username
        user.save()
        return JsonResponse({'new_username': username})


@login_required
def change_avatar(request):
    """修改头像"""

    new_avatar = request.FILES.get('new_avatar')

    customer = request.user
    old_avatar = customer.avatar
    if old_avatar != 'default/customers/avatars/2100_lab.jpg':
        old_avatar.delete()

    customer.avatar = new_avatar
    customer.save()

    return JsonResponse({'new_avatar': str(customer.avatar)})


@login_required
def get_customer_detail(request):
    """获取用户详情"""

    return JsonResponse(request.user.as_dict())


@login_required
def get_reward_coin(request):
    """获取奖励金余额"""

    return JsonResponse({'reward_coin': request.user.reward_coin})


@login_required
def get_learning_logs(request):
    """获取用户学习记录列表"""

    learning_logs = LearningLog.objects.filter(
        customer=request.user
    ).order_by('-latest_learn')
    return get_page(request, learning_logs)


@login_required
def get_order_logs(request):
    """获取用户订单记录列表"""

    order_logs = OrderLog.objects.filter(
        customer=request.user
    ).order_by('-created_at')
    return get_page(request, order_logs)


@login_required
def delete_customer(request):
    """用户删除自己"""

    user = request.user
    logout(request)
    delete_str = '_deleted_' + str(int(round(time.time() * 1000)))
    user.phone_number += delete_str
    user.username += delete_str
    user.save()
    user.delete()
    return JsonResponse({'message': INFO['object_deleted']})
