from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model


@login_required
def personal_center_main_page(request):
    user = request.user
    json_data = {
        'username': user.username,
        'avatar': str(user.avatar),
        'phone_number': user.phone_number,
        'reward_coin': user.reward_coin,
        'date_joined': user.date_joined
    }
    return JsonResponse(json_data)


@login_required
def personal_center_change_username(request):
    user = request.user
    username = request.POST.get('username')
    try:
        get_user_model().objects.get(username=username)
        return JsonResponse({'message': 'This username is already taken.'}, status=403)
    except get_user_model().DoesNotExist:
        user.username = username
        user.save()
        return JsonResponse({'username': username})
