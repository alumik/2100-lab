# pylint: disable=E1101

from django.conf import settings
from django.db import models

from core.constants import ADMIN_LOG_TEMPLATE


class AdminLog(models.Model):
    """管理员后台记录模型"""

    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_type = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    old_data = models.TextField(blank=True)
    new_data = models.TextField(blank=True)
    object_id = models.IntegerField()

    def transcript(self):
        """将数据库记录的日志信息转换成自然语言字符串"""

        return ADMIN_LOG_TEMPLATE[str(self.action_type)].substitute(
            object_id=self.object_id,
            old_data=self.old_data,
            new_data=self.new_data
        )

    def as_dict(self):
        """将模型转换为字典"""

        return {
            'admin_log_id': self.id,
            'created_at': self.created_at,
            'admin_username': self.admin_user.username,
            'message': self.transcript()
        }
