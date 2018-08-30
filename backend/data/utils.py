"""数据分析模块工具函数"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import Count

from courses.models import Course, CourseUpVotes
from customers.models import OrderLog, LearningLog


def get_customers_count(start_time, end_time):
    """获取一段时间内的新增用户数"""

    return get_user_model().all_objects.filter(
        date_joined__gte=start_time,
        date_joined__lte=end_time,
        is_staff=False
    ).count()


def get_income(start_time, end_time):
    """获取一段时间内的新增收入"""

    orders = OrderLog.objects.filter(
        created_at__gte=start_time,
        created_at__lte=end_time,
        refunded_at=None
    )
    income = Decimal('0.00')
    for order in orders:
        income += order.cash_spent
    return income


def get_courses_count(start_time, end_time):
    """获取一段时间内的新增课程数"""

    return Course.objects.filter(
        created_at__gte=start_time,
        created_at__lte=end_time
    ).count()


def get_orders_count(start_time, end_time):
    """获取一段时间内的新增订单数"""

    return OrderLog.objects.filter(
        created_at__gte=start_time,
        created_at__lte=end_time
    ).count()


def get_top_up_voted_courses(start_time, end_time):
    """获取近一段时间内点赞最多的五门课程"""

    courses_up_votes = CourseUpVotes.objects.filter(
        created_at__gte=start_time,
        created_at__lte=end_time
    ).values('course').annotate(total=Count('course')).order_by('-total')[:5]

    top_up_voted_courses = []
    for courses_up_vote in courses_up_votes:
        top_up_voted_courses.append(
            {
                'title': Course.all_objects.get(id=courses_up_vote['course']).title,
                'up_votes': courses_up_vote['total']
            }
        )

    return top_up_voted_courses


def get_top_learned_courses(start_time, end_time):
    """获取近一段时间内学习最多的五门课程"""

    learning_logs = LearningLog.objects.filter(
        latest_learn__gte=start_time,
        latest_learn__lte=end_time
    ).values('course').annotate(total=Count('course')).order_by('-total')[:5]

    top_learned_courses = []
    for learning_log in learning_logs:
        top_learned_courses.append(
            {
                'title': Course.all_objects.get(id=learning_log['course']).title,
                'learners': learning_log['total']
            }
        )

    return top_learned_courses
