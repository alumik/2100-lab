# pylint: disable=E1101

import datetime

from django.db import models
from django.conf import settings

from core.models import SoftDeletionModel


class Course(SoftDeletionModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    up_votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='course_up_vote_customer'
    )
    codename = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    reward_percent = models.DecimalField(decimal_places=2, max_digits=2, default=0)
    thumbnail = models.ImageField(upload_to='uploads/courses/thumbnails/', blank=True)
    audio = models.FileField(upload_to='uploads/courses/audios/', blank=True)
    expire_duration = models.DurationField(default=datetime.timedelta())
    can_comment = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def as_dict(self):
        return {
            'course_id': self.id,
            'thumbnail': str(self.thumbnail),
            'title': self.title,
            'description': self.description
        }
    
    def as_back_stage_dict(self):
        return {
            'codename': self.codename,
            'title': self.title,
            'price': self.price,
            'updated_at': self.updated_at
        }

    def is_free(self):
        return self.price == 0


class Image(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='uploads/courses/images/')
    load_time = models.IntegerField(default=0)

    def as_dict(self):
        return {
            'image_path': str(self.image_path),
            'load_time': self.load_time
        }


class Comment(SoftDeletionModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    up_votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='comment_up_vote_customer'
    )
    down_votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='comment_down_vote_customer'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.content) < 50:
            return self.content
        return self.content[:50] + '...'

    def as_dict(self):
        return {
            'comment_id': self.id,
            'username': self.user.username,
            'avatar': str(self.user.avatar),
            'course_id': self.course.id,
            'content': self.content,
            'up_votes': self.up_votes.count(),
            'down_votes': self.down_votes.count(),
            'created_at': self.created_at
        }


class Hero(models.Model):
    image = models.ImageField(upload_to='uploads/common/heroes/')
    caption = models.CharField(max_length=255, blank=True)

    def as_dict(self):
        return {
            'image': str(self.image),
            'caption': self.caption
        }
