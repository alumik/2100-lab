"""用户模块前台函数"""

import random
import re
import time

from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Comment out the following lines to prevent sms being sent by CI server.
#
# from qcloudsms_py.httpclient import HTTPError
# from customers.utils import tencent_cloud_message

from core.constants import ERROR, INFO
from core.utils import get_page
from customers.models import LearningLog, OrderLog


def get_verification_code(request):
    """获取短信验证码

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/forestage/auth/get-verification-code/

    **传入参数**

    ============ ==== ============
    参数         方法 说明
    ============ ==== ============
    phone_number POST 用户手机号码
    ============ ==== ============

    **返回值**

    HTTP400：手机号码无效

    .. code-block:: javascript

        {
            message: 'Not a valid phone number.'
        }

    HTTP200

    .. code-block:: javascript

        {
            is_new_customer: true // 是否是新用户
        }

    """

    phone_number = request.POST.get('phone_number')

    match = re.search(r'^1\d{10}$', phone_number)
    if not match:
        return JsonResponse({'message': ERROR['invalid_phone_number']}, status=400)

    verification_code = str(random.randint(0, 999999)).zfill(6)

    # Comment out the following lines to prevent sms being sent by CI server.
    #
    # try:
    #     tencent_cloud_message(phone_number, verification_code)
    # except (HTTPError, Exception):
    #     return JsonResponse(
    #         {'message': ERROR['message_send_failed']},
    #         status=500
    #     )

    request.session['prev_phone_number'] = phone_number
    request.session['verification_code'] = verification_code
    try:
        get_user_model().objects.get(phone_number=phone_number)
        new_customer = False
    except get_user_model().DoesNotExist:
        new_customer = True
    return JsonResponse(
        {
            # Comment out the following line to send real sms.
            'verification_code': verification_code,
            'is_new_customer': new_customer
        }
    )


def authenticate_customer(request):
    """认证用户

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/forestage/auth/authenticate-customer/

    **传入参数**

    ================= ==== ============
    参数              方法 说明
    ================= ==== ============
    phone_number      POST 用户手机号码
    verification_code POST 短信验证码
    ================= ==== ============

    **返回值**

    HTTP400：手机号码与之前不同

    .. code-block:: javascript

        {
            message: 'Different phone number.'
        }

    HTTP400：验证码不正确

    .. code-block:: javascript

        {
            message: 'Wrong verification code.'
        }

    HTTP200

    .. code-block:: javascript

        {
            is_new_customer: true,   // 是否是新用户
            customer.id,             // 用户ID
            username: 'John',        // 用户名
            avatar: 'uploads/1.png', // 用户头像路径
            is_staff: false          // 是否是管理员
        }

    """

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
            'avatar': str(user.avatar),
            'is_staff': user.is_staff
        }
    )


def get_eula(request):
    """获取最终用户许可协议

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/forestage/auth/get-eula/

    **传入参数**

    无

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            content: 'Test EULA.' // 协议内容
        }

    """

    return JsonResponse({'content': 'Test EULA.'})


@login_required
def change_username(request):
    """修改用户名

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/forestage/personal-center/change-username/

    **传入参数**

    ======== ==== ========
    参数     方法 说明
    ======== ==== ========
    username POST 新用户名
    ======== ==== ========

    **返回值**

    HTTP400：用户名重复

    .. code-block:: javascript

        {
            message: 'This username is already taken.'
        }

    HTTP400：用户名无效

    .. code-block:: javascript

        {
            message: 'Invalid username.'
        }

    HTTP200

    .. code-block:: javascript

        {
            new_username: 'John' // 新用户名
        }

    """

    username = request.POST.get('username')

    user = request.user
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
    """修改头像

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/forestage/personal-center/change-avatar/

    **传入参数**

    ========== ==== ======
    参数       方法 说明
    ========== ==== ======
    new_avatar POST 新头像
    ========== ==== ======

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            new_avatar: 'uploads/1.png' // 新头像
        }

    """

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
    """获取用户详情

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/forestage/personal-center/get-customer-detail/

    **传入参数**

    无

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            user_id: 1,                                      // 用户ID
            username: 'John',                                // 用户名
            phone_number: '12345678901',                     // 电话号码
            avatar: 'uploads/1.png',                         // 头像
            reward_coin: '100.00',                           // 奖励金余额
            is_vip: false,                                   // 是否是VIP
            is_banned: false,                                // 是否被禁言
            date_joined: '2018-08-31 16:46:44.794596+00:00', // 用户注册时间
            updated_at: '2018-08-31 16:46:44.794596+00:00'   // 最后修改时间
        }

    """

    return JsonResponse(request.user.as_dict())


@login_required
def get_reward_coin(request):
    """获取奖励金余额

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/personal-center/get-reward-coin/

    **传入参数**

    无

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            reward_coin: '100.00' // 奖励金余额
        }

    """

    return JsonResponse({'reward_coin': request.user.reward_coin})


@login_required
def get_learning_logs(request):
    """获取用户学习记录列表

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/personal-center/get-learning-logs/

    **传入参数**

    ========== ==== ================
    参数       方法 说明
    ========== ==== ================
    page       POST 当前页码
    page_limit POST 每页最大显示数量
    ========== ==== ================

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            'count': 2,
            'page': 2,
            'num_pages': 1,
            'content': [
                {
                    course_codename: 'SOFT001',                       // 课程代码
                    course_title: 'Data Structure',                   // 课程名
                    customer_username: 'John',                        // 用户名
                    latest_learn: '2018-08-31 16:46:44.794596+00:00', // 最后学习时间
                    expire_time: '2018-09-01 16:46:44.794596+00:00'   // 课程失效时间
                },
                ...
            ]
        }

    """

    learning_logs = LearningLog.objects.filter(
        customer=request.user
    ).order_by('-latest_learn')
    return get_page(request, learning_logs)


@login_required
def get_order_logs(request):
    """获取用户订单记录列表

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/personal-center/get-order-logs/

    **传入参数**

    ========== ==== ================
    参数       方法 说明
    ========== ==== ================
    page       POST 当前页码
    page_limit POST 每页最大显示数量
    ========== ==== ================

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            'count': 2,
            'page': 2,
            'num_pages': 1,
            'content': [
                {
                    order_no: '8acf2530-ad40-11e8-83f6-7c11cb55a985', // 订单号
                    course_codename: 'SOFT001',                       // 课程代码
                    course_title: 'Data Structure',                   // 课程名
                    customer_username: 'John',                        // 用户名
                    created_at: '2018-08-31 16:46:44.794596+00:00',   // 创建时间
                    money: '100.00',                                  // 成交金额
                    is_refunded: false                                // 是否已退款
                },
                ...
            ]
        }

    """

    order_logs = OrderLog.objects.filter(
        customer=request.user
    ).order_by('-created_at')
    return get_page(request, order_logs)


@login_required
def delete_customer(request):
    """用户删除自己

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/customers/personal-center/delete-customer/

    **传入参数**

    无

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            message: 'Object deleted.'
        }

    """

    user = request.user
    logout(request)
    delete_str = '_deleted_' + str(int(round(time.time() * 1000)))
    user.phone_number += delete_str
    user.username += delete_str
    user.save()
    user.delete()
    return JsonResponse({'message': INFO['object_deleted']})
