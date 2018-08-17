import re
import random

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import LearningLog, OrderLog
from core.utils import get_page


def get_verification_code(request):
    phone_number = request.POST.get('phone_number')
    match = re.search(r'^1\d{10}$', phone_number)
    if match:
        verification_code = str(random.randint(0, 999999)).zfill(6)
        request.session['prev_phone_number'] = phone_number
        request.session['verification_code'] = verification_code
        return JsonResponse({'verification_code': verification_code})
    else:
        return JsonResponse({'message': 'Not a valid phone number.'}, status=400)


def authenticate_customer(request):
    phone_number = request.POST.get('phone_number')
    verification_code = request.POST.get('verification_code')

    if phone_number != request.session['prev_phone_number']:
        return JsonResponse({'message': 'Different phone number.'}, status=401)

    if verification_code != request.session['verification_code']:
        return JsonResponse({'message': 'Wrong verification code.'}, status=401)

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
            'avatar': str(user.avatar)
        }
    )


def get_eula(request):
    return JsonResponse({'content': 'Test EULA.'})


@login_required
def personal_center_change_username(request):
    user = request.user
    username = request.POST.get('username')
    try:
        get_user_model().objects.get(username=username)
        return JsonResponse({'message': 'This username is already taken.'}, status=403)
    except get_user_model().DoesNotExist:
        if re.match(r'^.*_deleted_.*$', username):
            return JsonResponse({'message': 'Invalid username.'}, status=403)
        user.username = username
        user.save()
        return JsonResponse({'new_username': username})


@login_required
def personal_center_get_customer_detail(request):
    return JsonResponse(request.user.as_dict())


@login_required
def personal_center_get_learning_logs(request):
    learning_logs = LearningLog.objects.filter(customer=request.user).order_by('-latest_learn')
    return get_page(request, learning_logs)


@login_required
def personal_center_get_order_logs(request):
    order_logs = OrderLog.objects.filter(customer=request.user).order_by('-created_at')
    return get_page(request, order_logs)
