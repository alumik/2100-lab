from django.contrib import admin

from courses.models import Course, Image, Comment, Hero, CourseUpVotes

admin.site.register(Course)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Hero)
admin.site.register(CourseUpVotes)
