from django.contrib import admin
from .models import UserProfile, LearningLog, OrderLog

admin.site.register(UserProfile)
admin.site.register(LearningLog)
admin.site.register(OrderLog)
