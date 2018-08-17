from .models import Course
from customers.models import OrderLog


def get_courses(course_type, limit=None):
    if course_type == Course.TYPE_FREE:
        courses = Course.objects.filter(price='0.00').order_by('-modified_at')
    elif course_type == Course.TYPE_PAID:
        courses = Course.objects.exclude(price='0.00').order_by('-modified_at')
    else:
        courses = Course.objects.all().order_by('-modified_at')
    if limit:
        courses = courses[:limit]
    return courses


def can_access(course, customer):
    if int(course.price) == 0:
        return True
    try:
        OrderLog.objects.get(course=course, customer=customer, refunded_at=None)
        return True
    except OrderLog.DoesNotExist:
        return False
