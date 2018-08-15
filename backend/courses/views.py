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


def get_recent_courses(request):
    free_courses = Course.objects.filter(price='0.00').order_by('-modified_at')[:10]
    paid_courses = Course.objects.exclude(price='0.00').order_by('-modified_at')[:10]
    json_data = {
        'free_courses': [],
        'paid_courses': []
    }
    for free_course in free_courses:
        json_data['free_courses'].append(
            {
                'id': free_course.id,
                'thumbnail': str(free_course.thumbnail),
                'title': free_course.title,
                'description': free_course.description
            }
        )
    for paid_course in paid_courses:
        json_data['paid_courses'].append(
            {
                'id': paid_course.id,
                'thumbnail': str(paid_course.thumbnail),
                'title': paid_course.title,
                'description': paid_course.description
            }
        )
    return JsonResponse(json_data)
