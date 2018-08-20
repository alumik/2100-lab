from django.contrib import admin

from courses.models import Course, Image, Comment

admin.site.register(Course)
admin.site.register(Image)
admin.site.register(Comment)
