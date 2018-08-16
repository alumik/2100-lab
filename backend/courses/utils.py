from .models import Course


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
