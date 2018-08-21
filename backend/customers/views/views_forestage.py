import re
import random
import time

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.utils import get_page
from core.messages import ERROR
from customers.models import LearningLog, OrderLog


def get_verification_code(request):
    phone_number = request.POST.get('phone_number')
    match = re.search(r'^1\d{10}$', phone_number)
    if match:
        verification_code = str(random.randint(0, 999999)).zfill(6)
        request.session['prev_phone_number'] = phone_number
        request.session['verification_code'] = verification_code
        request.session['generate_time'] = round(time.time())
        try:
            get_user_model().objects.get(phone_number=phone_number)
            new_customer = False
        except get_user_model().DoesNotExist:
            new_customer = True
        return JsonResponse(
            {
                'verification_code': verification_code,
                'is_new_customer': new_customer
            }
        )
    return JsonResponse({'message': ERROR['invalid_phone_number']}, status=400)


def get_generate_time(request):
    json_data = {'generate_time': ''}
    if 'generate_time' in request.session:
        json_data['generate_time'] = request.session['generate_time']
    return JsonResponse(json_data)


def authenticate_customer(request):
    phone_number = request.POST.get('phone_number')
    verification_code = request.POST.get('verification_code')

    if phone_number != request.session['prev_phone_number']:
        return JsonResponse({'message': ERROR['different_phone_number']}, status=401)

    if verification_code != request.session['verification_code']:
        return JsonResponse({'message': ERROR['invalid_verification_code']}, status=401)

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
def change_username(request):
    user = request.user
    username = request.POST.get('username')
    try:
        get_user_model().objects.get(username=username)
        return JsonResponse({'message': ERROR['username_already_taken']}, status=403)
    except get_user_model().DoesNotExist:
        if re.match(r'^.*_deleted_.*$', username):
            return JsonResponse({'message': ERROR['invalid_username']}, status=403)
        user.username = username
        user.save()
        return JsonResponse({'new_username': username})


@login_required
def get_customer_detail(request):
    return JsonResponse(request.user.as_dict())


@login_required
def get_reward_coin(request):
    return JsonResponse({'reward_coin': request.user.reward_coin})


@login_required
def get_learning_logs(request):
    learning_logs = LearningLog.objects.filter(customer=request.user).order_by('-latest_learn')
    return get_page(request, learning_logs)


@login_required
def get_order_logs(request):
    order_logs = OrderLog.objects.filter(customer=request.user).order_by('-created_at')
    return get_page(request, order_logs)
