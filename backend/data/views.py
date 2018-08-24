from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse

from data import utils
from core.constants import ERROR


@login_required
def get_overall_data(request):
    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    days = request.GET.get('days', 1)

    end_time = timezone.now()
    start_time = timezone.now() - timezone.timedelta(days=int(days))

    customers_count = utils.get_customers_count(start_time, end_time)
    income = utils.get_income(start_time, end_time)
    courses_count = utils.get_courses_count(start_time, end_time)
    orders_count = utils.get_orders_count(start_time, end_time)
    top_up_voted_courses = utils.get_top_up_voted_courses(start_time, end_time)
    top_learned_courses = utils.get_top_learned_courses(start_time, end_time)

    return JsonResponse(
        {
            'customers_count': customers_count,
            'income': income,
            'courses_count': courses_count,
            'orders_count': orders_count,
            'top_up_voted_courses': top_up_voted_courses,
            'top_learned_courses': top_learned_courses
        }
    )
