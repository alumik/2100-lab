from django.http import JsonResponse
from django.contrib.auth import authenticate, login


def authenticate_admin(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'User is already authenticated.'}, status=400)

    phone_number = request.POST.get('phone_number')
    password = request.POST.get('password')

    admin = authenticate(request, phone_number=phone_number, password=password)

    if not admin:
        return JsonResponse({'message': 'Wrong phone number or password.'}, status=400)

    if not admin.is_staff:
        return JsonResponse({'message': 'Permission denied.'}, status=400)

    login(request, admin)
    json_data = {
        'permissions': [],
        'admin_id': admin.id,
        'username': admin.username
    }
    for group in admin.groups.all():
        json_data['permissions'].append(group.name)

    return JsonResponse(json_data)
