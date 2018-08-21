import re

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from core.messages import ERROR, INFO
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
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

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
    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

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


@login_required
def change_admin_username(request):
    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    admin_id = request.POST.get('admin_id')
    new_username = request.POST.get('new_username')

    try:
        admin = get_user_model().objects.get(id=admin_id, is_staff=True)
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    try:
        get_user_model().objects.get(username=new_username)
        return JsonResponse({'message': ERROR['username_already_taken']}, status=400)
    except get_user_model().DoesNotExist:
        if re.match(r'^.*_deleted_.*$', new_username):
            return JsonResponse({'message': ERROR['invalid_username']}, status=400)
        admin.username = new_username
        admin.save()
        return JsonResponse({'new_username': new_username})


@login_required
def change_admin_password(request):
    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    admin_id = request.POST.get('admin_id')
    new_password = request.POST.get('new_password')

    try:
        admin = get_user_model().objects.get(id=admin_id, is_staff=True)
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    admin.set_password(new_password)
    admin.save()
    return JsonResponse({'message': INFO['success']})


@login_required
def delete_admin(request):
    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    admin_id = request.POST.get('admin_id')

    try:
        admin = get_user_model().objects.get(id=admin_id, is_staff=True)
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    admin.delete()
    return JsonResponse({'message': INFO['object_deleted']})


@login_required
def add_admin(request):
    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    phone_number = request.POST.get('phone_number')
    password = request.POST.get('password')

    if not re.search(r'^1\d{10}$', phone_number):
        return JsonResponse({'message': ERROR['invalid_phone_number']}, status=400)

    if password == '':
        return JsonResponse({'message': ERROR['invalid_password']}, status=400)

    try:
        get_user_model().objects.get(phone_number=phone_number)
        return JsonResponse({'message': ERROR['admin_already_registered']}, status=400)
    except get_user_model().DoesNotExist:
        new_admin = get_user_model().objects.create_user(
            phone_number=phone_number,
            password=password,
            is_staff=True
        )
    return JsonResponse({'new_admin_id': new_admin.id})


@login_required
def change_admin_groups(request):
    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    new_admin_groups = request.POST.getlist('new_admin_groups', [])
    admin_id = request.POST.get('admin_id')

    try:
        admin = get_user_model().objects.get(id=admin_id, is_staff=True)
    except get_user_model().DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    admin.groups.clear()
    for admin_group in new_admin_groups:
        if admin_group != 'super_admin':
            admin.groups.add(Group.objects.get(name=admin_group))
    if 'super_admin' in new_admin_groups:
        admin.is_superuser = True
    admin.save()
    return JsonResponse({'message': INFO['success']})
