from django.conf import settings
from django.db import models

from courses.models import Course


class LearningLog(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    latest_learn = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('customer', 'course')

    def as_dict(self):
        return {
            'course_codename': self.course.codename,
            'course_title': self.course.title,
            'customer_username': self.customer.username,
            'latest_learn': self.latest_learn,
            'expire_time': self.expire_time
        }


class OrderLog(models.Model):
    order_no = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    cash_spent = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    reward_spent = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    payment_method = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    refunded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('customer', 'course')

    def as_dict(self):
        return {
            'order_no': self.order_no,
            'course_codename': self.course.codename,
            'course_title': self.course.title,
            'customer_username': self.customer.username,
            'created_at': self.created_at,
            'money': self.cash_spent + self.reward_spent,
            'is_refunded': self.refunded_at is not None
        }

    def as_backstage_dict(self):
        return {
            'order_id': self.id,
            'order_no': self.order_no,
            'course_codename': self.course.codename,
            'course_title': self.course.title,
            'customer_username': self.customer.username,
            'money': self.cash_spent + self.reward_spent,
            'is_refunded': self.refunded_at is not None
        }
