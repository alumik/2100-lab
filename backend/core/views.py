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
