"""课程模块模型"""

# pylint: disable=E1101

import datetime

from django.conf import settings
from django.db import models

from core.models import SoftDeletionModel


class Course(SoftDeletionModel):
    """课程模型"""

    title = models.CharField(max_length=100)
    description = models.TextField()
    up_votes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='course_up_votes',
        through='CourseUpVotes'
    )
    codename = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    reward_percent = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0
    )
    thumbnail = models.ImageField(
        upload_to='uploads/courses/thumbnails/',
        blank=True
    )
    audio = models.FileField(upload_to='uploads/courses/audios/', blank=True)
    expire_duration = models.DurationField(default=datetime.timedelta())
    can_comment = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    learners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='learners',
        through='customers.LearningLog'
    )

    def __str__(self):
        return self.title

    def as_dict(self):
        """获取字典"""

        return {
            'course_id': self.id,
            'thumbnail': str(self.thumbnail),
            'title': self.title,
            'description': self.description
        }

    def as_backstage_dict(self):
        """获取后台字典"""

        return {
            'course_id': self.id,
            'codename': self.codename,
            'title': self.title,
            'price': self.price,
            'updated_at': self.updated_at
        }

    def is_free(self):
        """判断课程是否为免费"""

        return self.price == 0


class CourseUpVotes(models.Model):
    """课程点赞记录模型"""

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    """课程图片资源模型"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to='uploads/courses/images/')
    load_time = models.IntegerField(default=0)

    def as_dict(self):
        """获取字典"""

        return {
            'image_id': self.id,
            'image_path': str(self.image_path),
            'load_time': self.load_time
        }


class Comment(SoftDeletionModel):
    """评论和回复模型"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
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
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.content) < 50:
            return self.content
        return self.content[:50] + '...'

    def as_dict(self, customer):
        """获取字典"""

        json_data = {
            'comment_id': self.id,
            'username': self.user.username,
            'user_id': self.user.id,
            'user_is_vip': self.user.is_vip,
            'avatar': str(self.user.avatar),
            'course_id': self.course.id,
            'content': self.content,
            'up_votes': self.up_votes.count(),
            'down_votes': self.down_votes.count(),
            'up_voted': customer in self.up_votes.all(),
            'down_voted': customer in self.down_votes.all(),
            'created_at': self.created_at,
            'reply_count': Comment.objects.filter(parent=self).count(),
            'replies': []
        }
        replies = Comment.objects.filter(
            parent=self
        ).order_by('-created_at')[:3]
        for reply in replies:
            json_data['replies'].append(reply.as_reply_dict(customer))
        return json_data

    def as_reply_dict(self, customer):
        """获取回复字典"""

        return {
            'comment_id': self.id,
            'username': self.user.username,
            'user_id': self.user.id,
            'user_is_vip': self.user.is_vip,
            'content': self.content,
            'up_votes': self.up_votes.count(),
            'down_votes': self.down_votes.count(),
            'up_voted': customer in self.up_votes.all(),
            'down_voted': customer in self.down_votes.all(),
            'created_at': self.created_at
        }

    def as_backstage_dict(self):
        """获取后台字典"""

        return {
            'comment_id': self.id,
            'created_at': self.created_at,
            'username': self.user.username,
            'course_codename': self.course.codename,
            'course_title': self.course.title,
            'content': self.content,
            'is_deleted': self.deleted_at is not None
        }


class Hero(models.Model):
    """头图模型"""

    image = models.ImageField(upload_to='uploads/common/heroes/')
    caption = models.CharField(max_length=255, blank=True)

    def as_dict(self):
        """获取字典"""

        return {
            'hero_id': self.id,
            'image': str(self.image),
            'caption': self.caption
        }
