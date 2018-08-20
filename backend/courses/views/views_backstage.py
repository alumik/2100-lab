from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse

from core.utils import get_back_stage_page
from courses.models import Course


@permission_required('courses.view_course')
def get_course_list(request):
    codename = request.GET.get('codename', '')
    title = request.GET.get('title', '')

    courses = Course.objects.filter(codename__contains=codename, title__contains=title).order_by('-updated_at')
    page = get_back_stage_page(request, courses)
    page['title'] = title
    page['codename'] = codename
    return JsonResponse(page, safe=False)


@permission_required('courses.view_course')
def get_course_detail(request):
    course_id = request.GET.get('course_id')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': 'Course not found.'}, status=404)

    return JsonResponse(
        {
            'course_id': course.id,
            'codename': course.codename,
            'title': course.title,
            'up_votes': course.up_votes.count(),
            'expire_duration': course.expire_duration,
            'price': course.price,
            'reward_percent': course.reward_percent,
            'created_at': course.created_at,
            'updated_at': course.updated_at,
            'description': course.description
        }
    )
