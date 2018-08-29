"""核心功能后台操作"""

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.constants import ERROR, INFO


def is_authenticated(request):
    """判断用户是否已登录

    如果已登录返回ID、登录状态和是否为管理员

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/core/auth/is-authenticated/

    **返回值**

    *成功：* HTTP200

    .. code-block:: javascript

        {
            user_id: 1,             // 用户ID
            is_authenticated: true, // 用户是否已登录
            is_staff: true,         // 用户是否是管理员
            admin_groups: [         // 用户权限组
                'course_admin',
                ...
            ]
        }

    """

    user = request.user
    admin_groups = []
    if user.is_staff:
        for group in user.groups.all():
            admin_groups.append(group.name)
        if user.is_superuser:
            admin_groups.append('super_admin')

    return JsonResponse(
        {
            'user_id': user.id,
            'is_authenticated': user.is_authenticated,
            'is_staff': user.is_staff,
            'admin_groups': admin_groups
        }
    )


@login_required
def logout(request):
    """注销用户

    **示例URL**

    .. code-block:: html

        http://localhost/api/v1/core/auth/logout/

    **返回值**

    *成功：* HTTP200

    .. code-block:: javascript

        {
            message: 'User logged out.'
        }

    """

    auth.logout(request)
    return JsonResponse({'message': INFO['user_logged_out']})
