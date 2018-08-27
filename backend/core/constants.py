from string import Template

INFO = {
    'object_deleted': 'Object deleted.',
    'user_logged_out': 'User logged out.',
    'success': 'Success.'
}

ERROR = {
    'access_denied': 'Access denied.',
    'object_not_found': 'Object not found.',
    'different_phone_number': 'Different phone number.',
    'invalid_phone_number': 'Not a valid phone number.',
    'invalid_username': 'Invalid username.',
    'invalid_verification_code': 'Wrong verification code.',
    'invalid_password': 'Invalid password.',
    'username_already_taken': 'This username is already taken.',
    'user_is_already_authenticated': 'User is already authenticated.',
    'invalid_phone_number_or_password': 'Invalid phone number or password.',
    'admin_already_registered': 'Admin is already registered.',
    'message_send_failed': 'Message send failed.',
    'course_already_purchased': 'This course has already been purchased.',
    'comment_not_allowed': 'Commenting is not allowed.'
}

ADMIN_GROUPS_NAME = {
    'super_admin': '超级管理员权限',
    'comment_admin': '留言管理权限',
    'course_admin': '课程管理权限',
    'customer_admin': '用户管理权限',
    'log_admin': '日志管理权限',
    'order_admin': '订单管理权限'
}

ACTION_TYPE = {
    'add_admin': 1,
    'change_admin_groups': 2,
    'update_admin_username': 3,
    'update_admin_password': 4,
    'delete_admin': 5,
    'refund_order': 6,
    'delete_customer': 7,
    'ban_customer_true': 8,
    'ban_customer_false': 9,
    'set_vip_true': 10,
    'set_vip_false': 11,
    'delete_comment': 12,
    'reply_comment': 13,
    'add_course': 14,
    'update_course': 15,
    'delete_course': 16
}

ADMIN_LOG_TEMPLATE = {
    '1': Template('新增了ID为 ${object_id} ，电话号码为 ${new_data} 的管理员'),
    '2': Template('将ID为 ${object_id} 的管理员的权限由 ${old_data} 改为 ${new_data}'),
    '3': Template('将ID为 ${object_id} 的管理员的用户名由 ${old_data} 改为 ${new_data}'),
    '4': Template('修改了ID为 ${object_id} 的管理员的密码'),
    '5': Template('删除了ID为 ${object_id} 的管理员'),
    '6': Template('为用户ID为 ${new_data} ，订单ID为 ${object_id} 的订单办理了退款'),
    '7': Template('删除了ID为 ${object_id} 的用户'),
    '8': Template('禁言了ID为 ${object_id} 的用户'),
    '9': Template('解除了ID为 ${object_id} 的用户的禁言'),
    '10': Template('认证了ID为 ${object_id} 的用户'),
    '11': Template('解除了ID为 ${object_id} 的用户的认证'),
    '12': Template('删除了ID为 ${object_id} 的留言'),
    '13': Template('回复了ID为 ${new_data} 的留言，新留言ID为 ${object_id}'),
    '14': Template('新增了ID为 ${object_id} 的课程'),
    '15': Template('修改了ID为 ${object_id} 的课程'),
    '16': Template('删除了ID为 ${object_id} 的课程')
}
