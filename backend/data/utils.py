from decimal import Decimal
import decimal

from django.contrib.auth import get_user_model
from django.db.models import Count

from customers.models import OrderLog, LearningLog
from courses.models import Course, CourseUpVotes


def get_customers_count(start_time, end_time):
    return get_user_model().all_objects.filter(
        date_joined__gte=start_time,
        date_joined__lte=end_time,
        is_staff=False
    ).count()


def get_income(start_time, end_time):
    orders = OrderLog.objects.filter(
        created_at__gte=start_time,
        created_at__lte=end_time,
        refunded_at=None
    )
    decimal.getcontext().prec = 2
    income = Decimal('0.00')
    for order in orders:
        income += order.cash_spent
    return income


def get_courses_count(start_time, end_time):
    return Course.objects.filter(
        created_at__gte=start_time,
        created_at__lte=end_time
    ).count()


def get_orders_count(start_time, end_time):
    return OrderLog.objects.filter(
        created_at__gte=start_time,
        created_at__lte=end_time
    ).count()


def get_top_up_voted_courses(start_time, end_time):
    courses_up_votes = CourseUpVotes.objects.filter(
        created_at__gte=start_time,
        created_at__lte=end_time
    ).values('course').annotate(total=Count('course')).order_by('-total')[:5]

    top_up_voted_courses = []
    for courses_up_vote in courses_up_votes:
        top_up_voted_courses.append(
            {
                'title': Course.objects.get(id=courses_up_vote['course']).title,
                'up_votes': courses_up_vote['total']
            }
        )

    return top_up_voted_courses


def get_top_learned_courses(start_time, end_time):
    learning_logs = LearningLog.objects.filter(
        latest_learn__gte=start_time,
        latest_learn__lte=end_time
    ).values('course').annotate(total=Count('course')).order_by('-total')[:5]

    top_learned_courses = []
    for learning_log in learning_logs:
        top_learned_courses.append(
            {
                'title': Course.objects.get(id=learning_log['course']).title,
                'learners': learning_log['total']
            }
        )

    return top_learned_courses
