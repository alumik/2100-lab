from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from core.utils import get_page
from customers.models import LearningLog
from courses.models import Hero, Course, Image, Comment
from courses.utils import get_courses, can_access, check_learning_log


def get_heroes(request):
    heroes = Hero.objects.all()
    count = heroes.count()
    json_data = {
        'count': count,
        'content': []
    }
    for hero in heroes:
        json_data['content'].append(hero.as_dict())
    return JsonResponse(json_data)


def get_recent_courses(request):
    free_courses = get_courses('free', 10)
    paid_courses = get_courses('paid', 10)
    json_data = {
        'free_courses': [],
        'paid_courses': []
    }
    for free_course in free_courses:
        json_data['free_courses'].append(free_course.as_dict())
    for paid_course in paid_courses:
        json_data['paid_courses'].append(paid_course.as_dict())
    return JsonResponse(json_data)


def get_course_list(request):
    courses = get_courses(request.GET.get('course_type')).order_by('-updated_at')
    return get_page(request, courses)


def get_course_detail(request):
    course_id = request.GET.get('course_id')
    request.session['referer_id'] = request.GET.get('referer_id', '')

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message', 'Course not found.'}, status=404)

    course_detail = {
        'course_id': course.id,
        'thumbnail': str(course.thumbnail),
        'title': course.title,
        'description': course.description,
        'price': course.price,
        'up_votes': course.up_votes.count(),
        'expire_duration': course.expire_duration,
        'expire_time': None,
        'can_access': False
    }
    if request.user.is_authenticated:
        try:
            learning_log = LearningLog.objects.get(course=course, customer=request.user)
            expire_time = learning_log.expire_time
            if expire_time is not None:
                course_detail['expire_time'] = expire_time
        except LearningLog.DoesNotExist:
            pass
        course_detail['can_access'] = can_access(course, request.user)
    return JsonResponse(course_detail)


@login_required
def up_vote_course(request):
    course_id = request.GET.get('course_id')
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'message': 'Course not found.'}, status=404)

    customer = request.user
    if customer in course.up_votes.all():
        up_voted = False
        course.up_votes.remove(customer)
    else:
        up_voted = True
        course.up_votes.add(customer)
    return JsonResponse(
        {
            'up_voted': up_voted,
            'up_votes': course.up_votes.count()
        }
    )


@login_required
def get_course_assets(request):
    try:
        course = Course.objects.get(id=request.GET.get('course_id'))
    except Course.DoesNotExist:
        return JsonResponse({'message': 'Course not found.'}, status=404)

    if not can_access(course, request.user):
        return JsonResponse({'message': 'Access denied.'}, status=403)

    progress = check_learning_log(course, request.user)
    images = Image.objects.filter(course=course).all().order_by('load_time')
    json_data = {
        'course_id': course.id,
        'title': course.title,
        'description': course.description,
        'audio': str(course.audio),
        'images': [],
        'progress': progress
    }
    for image in images:
        json_data['images'].append(image.as_dict())

    return JsonResponse(json_data)


@login_required
def save_learning_log(request):
    try:
        course = Course.objects.get(id=request.GET.get('course_id'))
    except Course.DoesNotExist:
        return JsonResponse({'message': 'Course not found.'}, status=404)

    if not can_access(course, request.user):
        return JsonResponse({'message': 'Access denied.'}, status=403)

    try:
        learning_log = LearningLog.objects.get(course=course, customer=request.user)
    except LearningLog.DoesNotExist:
        return JsonResponse({'message': 'Learning log not found.'}, status=404)

    learning_log.progress = request.GET.get('progress')
    learning_log.save()

    return JsonResponse({'message': 'Success.'})


@login_required
def get_course_comments(request):
    try:
        course = Course.objects.get(id=request.GET.get('course_id'))
    except Course.DoesNotExist:
        return JsonResponse({'message': 'Course not found.'}, status=404)

    if not can_access(course, request.user):
        return JsonResponse({'message': 'Access denied.'}, status=403)

    comments = Comment.objects.filter(course=course).order_by('-created_at')
    return get_page(request, comments)


@login_required
def delete_comment(request):
    try:
        comment = Comment.objects.get(id=request.GET.get('comment_id'))
    except Comment.DoesNotExist:
        return JsonResponse({'message': 'Comment not found.'}, status=404)

    if not request.user.id == comment.customer.id:
        return JsonResponse({'message': 'Access denied.'}, status=403)

    comment.delete()
    return JsonResponse({'message': 'Comment deleted.'})


@login_required
def up_vote_comment(request):
    customer = request.user

    try:
        comment = Comment.objects.get(id=request.GET.get('comment_id'))
    except Course.DoesNotExist:
        return JsonResponse({'message': 'Comment not found.'}, status=404)

    if not can_access(comment.course, customer):
        return JsonResponse({'message': 'Access denied.'}, status=403)

    if customer in comment.up_votes.all():
        up_voted = False
        comment.up_votes.remove(customer)
    else:
        up_voted = True
        comment.up_votes.add(customer)
    return JsonResponse(
        {
            'up_voted': up_voted,
            'up_votes': comment.up_votes.count()
        }
    )


@login_required
def down_vote_comment(request):
    customer = request.user

    try:
        comment = Comment.objects.get(id=request.GET.get('comment_id'))
    except Course.DoesNotExist:
        return JsonResponse({'message': 'Comment not found.'}, status=404)

    if not can_access(comment.course, customer):
        return JsonResponse({'message': 'Access denied.'}, status=403)

    if customer in comment.down_votes.all():
        down_voted = False
        comment.down_votes.remove(customer)
    else:
        down_voted = True
        comment.down_votes.add(customer)
    return JsonResponse(
        {
            'down_voted': down_voted,
            'down_votes': comment.down_votes.count()
        }
    )


@login_required
def add_comment(request):
    user = request.user

    try:
        course = Course.objects.get(id=request.GET.get('course_id'))
    except Course.DoesNotExist:
        return JsonResponse({'message': 'Course not found.'}, status=404)

    if not can_access(course, request.user):
        return JsonResponse({'message': 'Access denied.'}, status=403)

    Comment.objects.create(
        user=user,
        course=course,
        content=request.POST.get('content')
    )
    return JsonResponse({'message': 'Success.'})