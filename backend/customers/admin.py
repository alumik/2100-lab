from django.contrib import admin

from customers.models import LearningLog, OrderLog

admin.site.register(LearningLog)
admin.site.register(OrderLog)
