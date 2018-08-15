from django.http import JsonResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Heroes, Course
from customers.models import LearningLog


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
        json_data['free_courses'].append(free_course.as_brief_dict())
    for paid_course in paid_courses:
        json_data['paid_courses'].append(paid_course.as_brief_dict())
    return JsonResponse(json_data)


def get_free_course_list(request):
    course_objects = Course.objects.filter(price='0.00').order_by('-modified_at')
    count = course_objects.count()

    page = request.GET.get('page', request.POST['page'])
    paginator = Paginator(course_objects, request.POST['page_limit'])

    try:
        course_page = paginator.page(page)
    except PageNotAnInteger:
        course_page = paginator.page(request.POST['page'])
    except EmptyPage:
        course_page = paginator.page(paginator.num_pages)

    course_list = list(
        map(lambda course_object: course_object.as_brief_dict(), list(course_page))
    )
    return JsonResponse(
        {
            'count': count,
            'content': course_list
        },
        safe=False
    )


def get_paid_course_list(request):
    course_objects = Course.objects.exclude(price='0.00').order_by('-modified_at')
    count = course_objects.count()

    page = request.GET.get('page', request.POST['page'])
    paginator = Paginator(course_objects, request.POST['page_limit'])

    try:
        course_page = paginator.page(page)
    except PageNotAnInteger:
        course_page = paginator.page(request.POST['page'])
    except EmptyPage:
        course_page = paginator.page(paginator.num_pages)

    course_list = list(
        map(lambda course_object: course_object.as_brief_dict(), list(course_page))
    )
    return JsonResponse(
        {
            'count': count,
            'content': course_list
        },
        safe=False
    )


def get_course_detail(request):
    course_id = request.GET.get('id')
    referer_id = request.GET.get('ref', '')
    request.session['referer_id'] = referer_id
    course = Course.objects.get(id=course_id)
    course_detail = {
        'id': course.id,
        'thumbnail': str(course.thumbnail),
        'title': course.title,
        'description': course.description,
        'price': course.price,
        'up_votes': course.up_votes.count(),
        'expire_duration': course.expire_duration,
        'expire_time': None
    }
    if request.user.is_authenticated:
        try:
            learning_log = LearningLog.objects.get(course=course, customer=request.user)
            expire_time = learning_log.expire_time
            if expire_time is not None:
                course_detail['expire_time'] = expire_time
        except LearningLog.DoesNotExist:
            pass
    return JsonResponse(course_detail)
