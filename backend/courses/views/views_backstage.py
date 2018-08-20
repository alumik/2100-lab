from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse

from core.utils import get_backstage_page
from courses.models import Course, Comment


@permission_required('courses.view_course')
def get_course_list(request):
    codename = request.GET.get('codename', '')
    title = request.GET.get('title', '')

    courses = Course.objects.filter(codename__contains=codename, title__contains=title).order_by('-updated_at')
    page = get_backstage_page(request, courses)
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


@permission_required('courses.view_comment')
def get_comment_list(request):
    username = request.GET.get('username', '')
    course_codename = request.GET.get('course_codename', '')
    course_title = request.GET.get('course_title', '')
    is_deleted = request.GET.get('is_deleted', '0')

    comments = Comment.all_objects.filter(
        user__username__contains=username,
        course__codename__contains=course_codename,
        course__title__contains=course_title,
    ).order_by('-created_at')
    if is_deleted == '1':
        comments = comments.filter(deleted_at=None)
    elif is_deleted == '2':
        comments = comments.exclude(deleted_at=None)

    page = get_backstage_page(request, comments)
    page['username'] = username
    page['course_codename'] = course_codename
    page['course_title'] = course_title
    page['is_deleted'] = is_deleted
    return JsonResponse(page, safe=False)
