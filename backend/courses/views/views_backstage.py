from django.contrib.auth.decorators import permission_required

from core.utils import get_back_stage_page
from courses.models import Course


@permission_required('courses.view_course')
def get_course_list(request):
    codename = request.GET.get('codename', '')
    title = request.GET.get('title', '')

    courses = Course.objects.filter(codename__contains=codename, title__contains=title)
    return get_back_stage_page(request, courses)
