from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse

from core.utils import get_backstage_page
from core.messages import ERROR, INFO
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
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

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


@permission_required('courses.view_comment')
def get_comment_detail(request):
    comment_id = request.GET.get('comment_id')

    try:
        comment = Comment.all_objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    return JsonResponse(
        {
            'comment_id': comment.id,
            'created_at': comment.created_at,
            'username': comment.user.username,
            'course_codename': comment.course.codename,
            'course_title': comment.course.title,
            'is_deleted': True if comment.deleted_at is not None else False,
            'deleted_at': comment.deleted_at,
            'up_votes': comment.up_votes.count(),
            'down_votes': comment.down_votes.count(),
            'content': comment.content
        }
    )


@permission_required('courses.add_comment')
def add_comment(request):
    comment_content = request.POST.get('comment_content')
    course_codename = request.POST.get('course_codename')

    try:
        course = Course.objects.get(codename=course_codename)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    Comment.objects.create(
        user=request.user,
        course=course,
        content=comment_content
    )
    return JsonResponse({'message': INFO['success']})


@permission_required('courses.delete_comment')
def delete_comment(request):
    comment_id = request.GET.get('comment_id')

    try:
        comment = Comment.objects.get(id=comment_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': ERROR['object_not_found']}, status=404)

    comment.delete()
    return JsonResponse({'message': INFO['object_deleted']})
