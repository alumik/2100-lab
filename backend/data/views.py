"""数据分析模块操作"""

from datetime import datetime
import time
import pytz

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone

from core.constants import ERROR
from data import utils


@login_required
def get_overall_data(request):
    """数据分析第一页：获取总体数据"""

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


@login_required
def get_data_by_time(request):
    """数据分析第二页：获取时间对比数据"""

    if not request.user.is_superuser:
        return JsonResponse({'message': ERROR['access_denied']}, status=403)

    start_timestamp = request.GET.get('start_timestamp', round(time.time()))
    end_timestamp = request.GET.get('end_timestamp', round(time.time()))
    time_step = request.GET.get('time_step', 1)

    start_time = datetime.fromtimestamp(int(start_timestamp), tz=pytz.utc)
    end_time = datetime.fromtimestamp(int(end_timestamp), tz=pytz.utc)
    data = []

    right_time = end_time
    while right_time - timezone.timedelta(days=int(time_step)) >= start_time:
        left_time = right_time - timezone.timedelta(days=int(time_step))

        customers_count = utils.get_customers_count(left_time, right_time)
        income = utils.get_income(left_time, right_time)
        courses_count = utils.get_courses_count(left_time, right_time)
        orders_count = utils.get_orders_count(left_time, right_time)

        right_time = left_time

        data.append(
            {
                'right_time': right_time,
                'data': {
                    'customers_count': customers_count,
                    'income': income,
                    'courses_count': courses_count,
                    'orders_count': orders_count
                }
            }
        )

    return JsonResponse({'content': data})
