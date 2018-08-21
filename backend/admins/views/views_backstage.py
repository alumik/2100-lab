from django.http import JsonResponse
from django.contrib.auth import authenticate, login

from core.messages import ERROR


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
        'permissions': [],
        'admin_id': admin.id,
        'username': admin.username
    }
    for group in admin.groups.all():
        json_data['permissions'].append(group.name)

    return JsonResponse(json_data)
