from django.conf import settings
from django.db import models
from django.utils import timezone


class AdminLog(models.Model):
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_type = models.SmallIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    old_data = models.TextField()
    new_data = models.TextField()
    object_id = models.IntegerField()
