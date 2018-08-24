# pylint: disable=E1101

from django.conf import settings
from django.db import models

from core.constants import ADMIN_LOG_TEMPLATE


class AdminLog(models.Model):
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_type = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    old_data = models.TextField(blank=True)
    new_data = models.TextField(blank=True)
    object_id = models.IntegerField()

    def transcript(self):
        return ADMIN_LOG_TEMPLATE[str(self.action_type)].substitute(
            object_id=self.object_id,
            old_data=self.old_data,
            new_data=self.new_data
        )

    def as_dict(self):
        return {
            'admin_log_id': self.id,
            'created_at': self.created_at,
            'admin_username': self.admin_user.username,
            'message': self.transcript()
        }
