import time

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.messages import INFO


def is_authenticated(request):
    return JsonResponse({'is_authenticated': request.user.is_authenticated})


@login_required
def logout(request):
    auth.logout(request)
    return JsonResponse({'message': INFO['user_logged_out']})


@login_required
def delete_user(request):
    user = request.user
    auth.logout(request)
    user.phone_number += '_deleted_' + str(int(round(time.time() * 1000)))
    user.username = user.phone_number
    user.save()
    user.delete()
    return JsonResponse({'message': INFO['object_deleted']})
