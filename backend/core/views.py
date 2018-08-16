import time

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def is_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True})
    return JsonResponse({'is_authenticated': False})


@login_required
def logout(request):
    auth.logout(request)
    return JsonResponse({'message': 'User logged out.'})


@login_required
def delete_user(request):
    user = request.user
    auth.logout(request)
    user.phone_number += '_deleted_' + str(int(round(time.time() * 1000)))
    user.username = user.phone_number
    user.save()
    user.delete()
    return JsonResponse({'message': 'User deleted.'})
