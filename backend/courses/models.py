from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    up_votes = models.ManyToManyField(User, blank=True, related_name='course_up_vote_customer')
    codename = models.CharField(max_length=10)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    reward_percent = models.DecimalField(decimal_places=2, max_digits=2)
    thumbnail = models.ImageField(upload_to='./upload/courses/thumbnails/')
    audio = models.FileField(upload_to='./upload/courses/audios/')
    expire_duration = models.DurationField()
    can_comment = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if len(self.description) < 50:
            return self.description
        else:
            return self.description[:50] + '...'


class Image(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='./upload/courses/images/')
    load_time = models.IntegerField(default=0)


class Comment(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    up_votes = models.ManyToManyField(User, blank=True, related_name='comment_up_vote_customer')
    down_votes = models.ManyToManyField(User, blank=True, related_name='comment_down_vote_customer')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if len(self.content) < 50:
            return self.content
        else:
            return self.content[:50] + '...'
