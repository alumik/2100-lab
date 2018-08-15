from django.http import JsonResponse

from .models import Heroes, Course


def get_heroes(request):
    heroes = Heroes.objects.all()
    count = heroes.count()
    json_data = {
        'count': count,
        'content': []
    }
    for hero in heroes:
        json_data['content'].append(hero.as_dict())
    return JsonResponse(json_data)
