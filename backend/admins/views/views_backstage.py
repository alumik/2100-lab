"""管理员模块后台操作"""

from datetime import datetime
import time
import re
import pytz

from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.http import JsonResponse

from admins.models import AdminLog
from admins.utils import get_admin_page
from core.constants import ERROR, INFO, ACTION_TYPE, ADMIN_GROUPS_NAME
from core.utils import get_page


def authenticate_admin(request):
    """管理员登录

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/admin/backstage/auth/authenticate-admin/

    **传入参数/方法**

    ============ ==== ========
    参数         方法 说明
    ============ ==== ========
    phone_number POST 电话号码
    password     POST 密码
    ============ ==== ========

    **返回值**

    HTTP400：用户已登录

    .. code-block:: javascript

        {
            message: 'User is already authenticated.'
        }

    HTTP400：电话号码或密码错误

    .. code-block:: javascript

        {
            message: 'Invalid phone number or password.'
        }

    HTTP403：用户没有管理员权限

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP200

    .. code-block:: javascript

        {
            admin_id: 1,          // 管理员ID
            username: 'John',     // 管理员名称
            admin_groups: [       // 管理员权限组
                'customer_admin',
                ...
            ]
        }

    """

    phone_number = request.POST.get('phone_number')
    password = request.POST.get('password')

    if request.user.is_authenticated:
        return JsonResponse(
            {'message': ERROR['user_is_already_authenticated']},
            status=400
        )

    admin = authenticate(request, phone_number=phone_number, password=password)

    if not admin:
        return JsonResponse(
            {'message': ERROR['invalid_phone_number_or_password']},
            status=400
        )

    if not admin.is_staff:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    login(request, admin)
    json_data = {
        'admin_id': admin.id,
        'username': admin.username,
        'admin_groups': []
    }
    for group in admin.groups.all():
        json_data['admin_groups'].append(group.name)
    if admin.is_superuser:
        json_data['admin_groups'].append('super_admin')

    return JsonResponse(json_data)


@login_required
def get_admin_list(request):
    """获取所有管理员列表

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/admin/backstage/admin-management/get-admin-list/

    **传入参数/方法**

    ============ ==== ==================
    参数         方法 说明
    ============ ==== ==================
    phone_number GET  筛选参数：电话号码
    username     GET  筛选参数：用户名
    page         GET  当前页码
    page_limit   GET  每页最大显示数量
    ============ ==== ==================

    **返回值**

    HTTP403：管理员权限不足

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP200

    .. code-block:: javascript

        {
            phone_number: '123',                // 筛选参数：电话号码
            username: 'John',                   // 筛选参数：用户名
            count: 8,                           // 总条目数
            page: 1,                            // 当前页码
            num_pages: 12,                      // 总页码数
            content: [
                {
                    admin_id: 12,               // 管理员ID
                    username: 'John Smith',     // 管理员名称
                    phone_number: '12345678901' // 管理员电话号码
                },
                ...
            ]
        }

    """

    username = request.GET.get('username', '')
    phone_number = request.GET.get('phone_number', '')

    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    admins = get_user_model().objects.filter(
        is_staff=True,
        username__contains=username,
        phone_number__contains=phone_number
    ).order_by('-updated_at')
    page = get_admin_page(request, admins)
    page['username'] = username
    page['phone_number'] = phone_number
    return JsonResponse(page, safe=False)


@login_required
def get_admin_detail(request):
    """获取管理员详情

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/admin/backstage/admin-management/get-admin-detail/

    **传入参数/方法**

    ======== ==== ================
    参数     方法 说明
    ======== ==== ================
    admin_id GET  要查询的管理员ID
    ======== ==== ================

    **返回值**

    HTTP403：管理员权限不足

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP404：管理员未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            admin_id: 1,                                     // 管理员ID
            username: 'John',                                // 管理员名称
            phone_number: '12345678901',                     // 电话号码
            date_joined: '2018-08-31 16:46:44.794596+00:00', // 注册时间
            updated_at: '2018-08-31 16:46:44.794596+00:00',  // 修改时间
            admin_groups: [                                  // 管理员权限组
                'customer_admin',
                ...
            ]
        }

    """

    admin_id = request.GET.get('admin_id')

    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    try:
        admin = get_user_model().objects.get(id=admin_id, is_staff=True)
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    json_data = {
        'admin_id': admin.id,
        'username': admin.username,
        'phone_number': admin.phone_number,
        'date_joined': admin.date_joined,
        'updated_at': admin.updated_at,
        'admin_groups': []
    }
    for group in admin.groups.all():
        json_data['admin_groups'].append(group.name)
    if admin.is_superuser:
        json_data['admin_groups'].append('super_admin')

    return JsonResponse(json_data)


@login_required
def change_admin_username(request):
    """修改管理员用户名

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/admin/backstage/admin-management/change-admin-username/

    **传入参数/方法**

    ============ ==== ========
    参数         方法 说明
    ============ ==== ========
    admin_id     POST 管理员ID
    new_username POST 新用户名
    ============ ==== ========

    **返回值**

    HTTP403：管理员权限不足

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP404：管理员未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

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

    admin_id = request.POST.get('admin_id')
    new_username = request.POST.get('new_username')

    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    try:
        admin = get_user_model().objects.get(id=admin_id, is_staff=True)
        old_username = admin.username
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    try:
        get_user_model().objects.get(username=new_username)
        return JsonResponse(
            {'message': ERROR['username_already_taken']},
            status=400
        )

    except get_user_model().DoesNotExist:
        if re.match(r'^.*_deleted_.*$', new_username):
            return JsonResponse(
                {'message': ERROR['invalid_username']},
                status=400
            )
        admin.username = new_username
        admin.save()
        AdminLog.objects.create(
            admin_user=request.user,
            action_type=ACTION_TYPE['update_admin_username'],
            old_data=old_username,
            new_data=new_username,
            object_id=admin_id
        )
        return JsonResponse({'new_username': new_username})


@login_required
def change_admin_password(request):
    """修改管理员密码

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/admin/backstage/admin-management/change-admin-password/

    **传入参数/方法**

    ============ ==== ========
    参数         方法 说明
    ============ ==== ========
    admin_id     POST 管理员ID
    new_password POST 新密码
    ============ ==== ========

    **返回值**

    HTTP403：管理员权限不足

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP404：管理员未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Success.'
        }

    """

    admin_id = request.POST.get('admin_id')
    new_password = request.POST.get('new_password')

    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    try:
        admin = get_user_model().objects.get(id=admin_id, is_staff=True)
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    admin.set_password(new_password)
    admin.save()
    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['update_admin_password'],
        object_id=admin_id
    )
    return JsonResponse({'message': INFO['success']})


@login_required
def delete_admin(request):
    """删除管理员

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/admin/backstage/admin-management/delete-admin/

    **传入参数/方法**

    ======== ==== ========
    参数     方法 说明
    ======== ==== ========
    admin_id POST 管理员ID
    ======== ==== ========

    **返回值**

    HTTP403：管理员权限不足

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP404：管理员未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Object deleted.'
        }

    """

    admin_id = request.POST.get('admin_id')

    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    try:
        admin = get_user_model().objects.get(id=admin_id, is_staff=True)
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    delete_str = '_deleted_' + str(int(round(time.time() * 1000)))
    admin.phone_number += delete_str
    admin.username += delete_str

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['delete_admin'],
        object_id=admin_id
    )
    admin.delete()
    return JsonResponse({'message': INFO['object_deleted']})


@login_required
def add_admin(request):
    """添加管理员

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/admin/backstage/admin-management/add-admin/

    **传入参数/方法**

    ============ ==== ========
    参数         方法 说明
    ============ ==== ========
    phone_number POST 电话号码
    password     POST 密码
    ============ ==== ========

    **返回值**

    HTTP403：管理员权限不足

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP400：手机号码无效

    .. code-block:: javascript

        {
            message: 'Not a valid phone number.'
        }

    HTTP400：密码无效

    .. code-block:: javascript

        {
            message: 'Invalid password.'
        }

    HTTP400：管理员已存在

    .. code-block:: javascript

        {
            message: 'Admin is already registered.'
        }

    HTTP200

    .. code-block:: javascript

        {
            new_admin_id: 2 // 新管理员ID
        }

    """

    phone_number = request.POST.get('phone_number')
    password = request.POST.get('password')

    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    if not re.search(r'^1\d{10}$', phone_number):
        return JsonResponse(
            {'message': ERROR['invalid_phone_number']},
            status=400
        )

    if password == '':
        return JsonResponse({'message': ERROR['invalid_password']}, status=400)

    try:
        get_user_model().objects.get(phone_number=phone_number)
        return JsonResponse(
            {'message': ERROR['admin_already_registered']},
            status=400
        )
    except get_user_model().DoesNotExist:
        new_admin = get_user_model().objects.create_user(
            phone_number=phone_number,
            password=password,
            is_staff=True
        )

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['add_admin'],
        new_data=phone_number,
        object_id=new_admin.id
    )
    return JsonResponse({'new_admin_id': new_admin.id})


@login_required
def change_admin_groups(request):
    """修改管理员权限组

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/admin/backstage/admin-management/change-admin-groups/

    **传入参数/方法**

    ================ ==== ==============
    参数             方法 说明
    ================ ==== ==============
    admin_id         POST 管理员ID
    new_admin_groups POST 新管理员权限组
    ================ ==== ==============

    **返回值**

    HTTP403：管理员权限不足

    .. code-block:: javascript

        {
            message: 'Access denied.'
        }

    HTTP404：管理员未找到

    .. code-block:: javascript

        {
            message: 'Object not found.'
        }

    HTTP200

    .. code-block:: javascript

        {
            message: 'Success.'
        }

    """

    new_admin_groups = request.POST.getlist('new_admin_groups', [])
    admin_id = request.POST.get('admin_id')

    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    try:
        admin = get_user_model().objects.get(id=admin_id, is_staff=True)
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    old_admin_groups_cn = []
    new_admin_groups_cn = []
    for admin_group in admin.groups.all():
        old_admin_groups_cn.append(ADMIN_GROUPS_NAME[str(admin_group)])
    for admin_group in new_admin_groups:
        new_admin_groups_cn.append((ADMIN_GROUPS_NAME[str(admin_group)]))
    old_data = '，'.join(old_admin_groups_cn)
    new_data = '，'.join(new_admin_groups_cn)
    if old_data == '':
        old_data = '无权限'
    if new_data == '':
        new_data = '无权限'

    admin.groups.clear()
    for admin_group in new_admin_groups:
        admin.groups.add(Group.objects.get(name=admin_group))
    admin.save()

    AdminLog.objects.create(
        admin_user=request.user,
        action_type=ACTION_TYPE['change_admin_groups'],
        old_data=old_data,
        new_data=new_data,
        object_id=admin_id
    )
    return JsonResponse({'message': INFO['success']})


@permission_required('admins.view_adminlog')
def get_admin_log(request):
    """获取管理员操作日志

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/admin/backstage/log-management/get-admin-log/

    **传入参数/方法**

    ============== ==== ====================
    参数           方法 说明
    ============== ==== ====================
    admin_username GET  筛选参数：管理员名称
    filters        GET  筛选参数：查询项
    page           GET  当前页码
    page_limit     GET  每页最大显示数量
    ============== ==== ====================

    **返回值**

    HTTP200

    .. code-block:: javascript

        {
            count: 2,                                               // 总条目数
            page: 1,                                                // 当前页码
            num_pages: 2,                                           // 总页码数
            content: [
                {
                    admin_log_id: 1,                                // 日志ID
                    created_at: '2018-08-31 16:46:44.794596+00:00', // 创建日期
                    admin_username: 'John',                        // 管理员名称
                    message: '...'                                  // 日志内容
                },
                ...
            ]
        }

    """

    admin_username = request.GET.get('admin_username', '')
    start_timestamp = request.GET.get('start_timestamp', round(time.time()))
    end_timestamp = request.GET.get('end_timestamp', round(time.time()))
    filters = request.GET.getlist('filters', [])

    start_date_time = datetime.fromtimestamp(int(start_timestamp), tz=pytz.utc)
    end_date_time = datetime.fromtimestamp(int(end_timestamp), tz=pytz.utc)

    admin_logs = AdminLog.objects.filter(
        admin_user__username__contains=admin_username,
        created_at__gte=start_date_time,
        created_at__lte=end_date_time,
        action_type__in=filters
    ).order_by('-created_at')

    return get_page(request, admin_logs)
