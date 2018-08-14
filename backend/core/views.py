from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from random import randint
import re


def get_verification_code(request):
    phone_number = request.POST.get('phone_number')
    match = re.search(r'^\d{11}$', phone_number)
    if match:
        verification_code = str(randint(0, 999999)).zfill(6)
        request.session['verification_code'] = verification_code
        return JsonResponse({'verification_code': verification_code})
    else:
        return JsonResponse({'message': 'Not a valid phone number.'}, status=400)


def authenticate(request):
    phone_number = request.POST.get('phone_number')
    verification_code = request.POST.get('verification_code')

    if verification_code == request.session['verification_code']:
        try:
            user = get_user_model().objects.get(phone_number=phone_number)
            new_user = False
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create_user(phone_number=phone_number)
            new_user = True
        auth.login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
        del request.session['verification_code']
        return JsonResponse({'new_user': new_user})
    else:
        del request.session['verification_code']
        return JsonResponse({'message': 'Wrong verification code.'}, status=401)


def get_eula(request):
    return JsonResponse({'content': 'Test EULA.'})


@login_required
def logout(request):
    auth.logout(request)
    return JsonResponse({'message': 'User logged out.'})


def is_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True})
    return JsonResponse({'is_authenticated': False})
