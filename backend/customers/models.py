from django.db import models
from django.utils import timezone
from django.conf import settings

from courses.models import Course


class LearningLog(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('customer', 'course')

    def as_dict(self):
        return {
            'course_codename': self.course.codename,
            'course_title': self.course.title,
            'start_time': self.created_at,
            'expire_time': self.expire_time
        }


class OrderLog(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    cash_spent = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    reward_spent = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    payment_method = models.SmallIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    refunded_at = models.DateTimeField(default=timezone.now)
