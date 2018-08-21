from django.http import JsonResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import permission_required, login_required

from core.messages import ERROR
from admins.utils import get_admin_page


def authenticate_admin(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': ERROR['user_is_already_authenticated']}, status=400)

    phone_number = request.POST.get('phone_number')
    password = request.POST.get('password')

    admin = authenticate(request, phone_number=phone_number, password=password)

    if not admin:
        return JsonResponse({'message': ERROR['invalid_phone_number_or_password']}, status=400)

    if not admin.is_staff:
        return JsonResponse({'message': ERROR['access_denied']}, status=400)

    login(request, admin)
    json_data = {
        'admin_id': admin.id,
        'username': admin.username,
        'roles': []
    }
    for group in admin.groups.all():
        json_data['roles'].append(group.name)
    if admin.is_superuser:
        json_data['roles'].append('super_admin')

    return JsonResponse(json_data)


@login_required
def get_admin_list(request):
    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    username = request.GET.get('username', '')
    phone_number = request.GET.get('phone_number', '')

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
    admin_id = request.GET.get('admin_id')

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
        'roles': []
    }
    for group in admin.groups.all():
        json_data['roles'].append(group.name)
    if admin.is_superuser:
        json_data['roles'].append('super_admin')

    return JsonResponse(json_data)
