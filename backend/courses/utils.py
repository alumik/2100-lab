"""课程模块工具函数"""

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.utils import timezone

from courses.models import Course
from customers.models import LearningLog, OrderLog


def get_courses(course_type, limit=None):
    """获取课程"""

    if course_type == 'free':
        courses = Course.objects.filter(price='0.00').order_by('-updated_at')
    elif course_type == 'paid':
        courses = Course.objects.exclude(price='0.00').order_by('-updated_at')
    else:
        courses = Course.objects.all().order_by('-updated_at')
    if limit:
        courses = courses[:limit]
    return courses


def can_access(course, customer):
    """判断课程是否能够访问"""

    if course.is_free():
        return True
    try:
        OrderLog.objects.get(course=course, customer=customer, refunded_at=None)
        return True
    except OrderLog.DoesNotExist:
        return False


def check_learning_log(course, customer):
    """检查是否有学习记录，有就更新，没有就创建"""

    try:
        learning_log = LearningLog.objects.get(course=course, customer=customer)
        learning_log.latest_learn = timezone.now()
        learning_log.save()
    except LearningLog.DoesNotExist:
        learning_log = LearningLog.objects.create(
            course=course,
            customer=customer,
            expire_time=course.expire_duration + timezone.now()
        )
    return learning_log.progress


def get_comment_page(request, items):
    """评论分页工具函数"""

    count = items.count()
    page = request.GET.get('page')
    paginator = Paginator(items, request.GET.get('page_limit', 10))
    try:
        item_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        item_page = paginator.page(1)
    item_list = list(
        map(lambda item: item.as_dict(customer=request.user), list(item_page))
    )
    return JsonResponse(
        {
            'count': count,
            'page': item_page.number,
            'num_pages': paginator.num_pages,
            'content': item_list
        },
        safe=False
    )


def get_reply_page(request, items):
    """回复分页工具函数"""

    count = items.count()
    page = request.GET.get('page')
    paginator = Paginator(items, request.GET.get('page_limit', 10))
    try:
        item_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        item_page = paginator.page(1)
    item_list = list(
        map(
            lambda item: item.as_reply_dict(customer=request.user),
            list(item_page)
        )
    )
    return JsonResponse(
        {
            'count': count,
            'page': item_page.number,
            'num_pages': paginator.num_pages,
            'content': item_list
        },
        safe=False
    )
