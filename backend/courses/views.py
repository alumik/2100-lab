from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Hero, Course, Image, Comment
from .utils import get_courses, can_access
from core.utils import get_page
from customers.models import LearningLog


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
    free_courses = get_courses(Course.TYPE_FREE, 10)
    paid_courses = get_courses(Course.TYPE_PAID, 10)
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
    courses = get_courses(int(request.POST.get('course_type')))
    return get_page(request, courses)


def get_customer_course_detail(request):
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
        'is_paid': False
    }
    if request.user.is_authenticated:
        try:
            learning_log = LearningLog.objects.get(course=course, customer=request.user)
            expire_time = learning_log.expire_time
            if expire_time is not None:
                course_detail['expire_time'] = expire_time
        except LearningLog.DoesNotExist:
            pass
        course_detail['is_paid'] = can_access(course, request.user)
    return JsonResponse(course_detail)


@login_required
def up_vote_course(request):
    course_id = request.POST.get('course_id')
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
    course = Course.objects.get(id=request.POST.get('course_id'))
    if not can_access(course, request.user):
        return JsonResponse({'message': 'Access denied.'}, status=403)

    images = Image.objects.filter(course=course).all().order_by('load_time')
    json_data = {
        'course_id': course.id,
        'title': course.title,
        'description': course.description,
        'audio': str(course.audio),
        'images': []
    }
    for image in images:
        json_data['images'].append(image.as_dict())

    return JsonResponse(json_data)


@login_required
def get_course_comments(request):
    course = Course.objects.get(id=request.POST.get('course_id'))
    if not can_access(course, request.user):
        return JsonResponse({'message': 'Access denied.'}, status=403)

    comments = Comment.objects.filter(course=course)