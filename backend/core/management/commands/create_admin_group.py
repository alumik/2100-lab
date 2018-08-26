"""创建权限组并分配对应权限"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """控制台命令类"""

    def handle(self, *args, **options):
        """创建权限组并分配对应权限"""

        course_admin = Group.objects.create(name='course_admin')
        comment_admin = Group.objects.create(name='comment_admin')
        customer_admin = Group.objects.create(name='customer_admin')
        order_admin = Group.objects.create(name='order_admin')
        log_admin = Group.objects.create(name='log_admin')

        course_admin.permissions.add(*list(Permission.objects.filter(codename__contains='course')))
        course_admin.permissions.add(*list(Permission.objects.filter(codename__contains='hero')))
        course_admin.permissions.add(*list(Permission.objects.filter(codename__contains='image')))

        comment_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='comment'))
        )

        customer_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='customuser'))
        )
        customer_admin.permissions.add(
            *list(Permission.objects.filter(codename__contains='learninglog'))
        )

        order_admin.permissions.add(*list(Permission.objects.filter(codename__contains='orderlog')))

        log_admin.permissions.add(*list(Permission.objects.filter(codename__contains='adminlog')))

        course_admin.save()
        comment_admin.save()
        customer_admin.save()
        order_admin.save()
        log_admin.save()
