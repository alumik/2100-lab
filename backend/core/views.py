"""核心功能后台操作"""

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.constants import INFO


def is_authenticated(request):
    """判断用户是否已登录

    如果已登录返回ID、登录状态和是否为管理员
    """

    user = request.user
    return JsonResponse(
        {
            'user_id': user.id,
            'is_authenticated': user.is_authenticated,
            'is_staff': user.is_staff
        }
    )


@login_required
def logout(request):
    """注销用户"""

    auth.logout(request)
    return JsonResponse({'message': INFO['user_logged_out']})
