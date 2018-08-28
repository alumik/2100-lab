"""核心功能后台操作"""

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.constants import ERROR, INFO


def is_authenticated(request):
    """判断用户是否已登录

    如果已登录返回ID、登录状态和是否为管理员
    """

    user = request.user
    admin_groups = []
    if user.is_staff:
        try:
            admin = get_user_model().objects.get(id=user.id, is_staff=True)
        except get_user_model().DoesNotExist:
            return JsonResponse({'message': ERROR['object_not_found']}, status=404)
        for group in admin.groups.all():
            admin_groups.append(group.name)
        if admin.is_superuser:
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
    """注销用户"""

    auth.logout(request)
    return JsonResponse({'message': INFO['user_logged_out']})
