from django.utils import timezone

from .models import Course
from customers.models import LearningLog, OrderLog


def get_courses(course_type, limit=None):
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
    if course.is_free():
        return True
    try:
        OrderLog.objects.get(course=course, customer=customer, refunded_at=None)
        return True
    except OrderLog.DoesNotExist:
        return False


def check_learning_log(course, customer):
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
