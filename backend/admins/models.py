# pylint: disable=E1101

from django.conf import settings
from django.db import models

from core.constants import ACTION_TYPE


class AdminLog(models.Model):
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_type = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    old_data = models.TextField(blank=True)
    new_data = models.TextField(blank=True)
    object_id = models.IntegerField()

    def transcript(self):
        msg = ''
        if self.action_type == ACTION_TYPE['add_admin']:
            msg = '新增了ID为 ' \
                  + str(self.object_id) \
                  + ' ，电话号码为 ' \
                  + str(self.new_data) \
                  + ' 的管理员'
        elif self.action_type == ACTION_TYPE['change_admin_groups']:
            msg = '将ID为 ' \
                  + str(self.object_id) \
                  + ' 的管理员的权限由 ' \
                  + self.old_data \
                  + ' 改为 ' \
                  + self.new_data
        elif self.action_type == ACTION_TYPE['update_admin']:
            if self.new_data == '':
                msg = '修改了ID为 ' \
                      + str(self.object_id) \
                      + ' 的管理员的密码'
            else:
                msg = '将ID为 ' \
                      + str(self.object_id) \
                      + ' 的管理员的用户名由 ' \
                      + self.old_data \
                      + ' 改为 ' \
                      + self.new_data
        elif self.action_type == ACTION_TYPE['delete_admin']:
            msg = '删除了ID为 ' \
                  + str(self.object_id) \
                  + ' 的管理员'
        elif self.action_type == ACTION_TYPE['refund_order']:
            msg = '为用户ID为 ' \
                  + self.new_data \
                  + ' ，订单ID为 ' \
                  + str(self.object_id) \
                  + ' 的订单办理了退款'
        elif self.action_type == ACTION_TYPE['delete_customer']:
            msg = '删除了ID为 ' \
                  + str(self.object_id) \
                  + ' 的用户'
        elif self.action_type == ACTION_TYPE['ban_customer']:
            if self.new_data == 'True':
                msg = '禁言了ID为 ' \
                      + str(self.object_id) \
                      + ' 的用户'
            else:
                msg = '解除了ID为 ' \
                      + str(self.object_id) \
                      + ' 的用户的禁言'
        elif self.action_type == ACTION_TYPE['set_vip']:
            if self.new_data == 'True':
                msg = '认证了ID为 ' \
                      + str(self.object_id) \
                      + ' 的用户'
            else:
                msg = '解除了ID为 ' \
                      + str(self.object_id) \
                      + ' 的用户的认证'
        elif self.action_type == ACTION_TYPE['delete_comment']:
            msg = '删除了ID为 ' \
                  + str(self.object_id) \
                  + ' 的留言'
        elif self.action_type == ACTION_TYPE['reply_comment']:
            msg = '回复了ID为 ' \
                  + self.new_data \
                  + ' 的课程下的留言，新留言ID为 ' \
                  + str(self.object_id)
        elif self.action_type == ACTION_TYPE['add_course']:
            msg = '新增了ID为 ' \
                  + str(self.object_id) \
                  + ' 的课程'
        elif self.action_type == ACTION_TYPE['update_course']:
            msg = '修改了ID为 ' \
                  + str(self.object_id) \
                  + ' 的课程'
        elif self.action_type == ACTION_TYPE['delete_course']:
            msg = '删除了ID为 ' \
                  + str(self.object_id) \
                  + ' 的课程'
        return msg

    def as_dict(self):
        return {
            'admin_log_id': self.id,
            'created_at': self.created_at,
            'admin_username': self.admin_user.username,
            'message': self.transcript()
        }
