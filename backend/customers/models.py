from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from courses.models import Course
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='./upload/customers/avatars/')
    phone_validator = RegexValidator(regex=r'^\d{11}$', message='请输入一个有效的电话号码！')
    phone_number = models.CharField(validators=[phone_validator], max_length=11)
    reward_coin = models.DecimalField(decimal_places=2, max_digits=12)
    is_vip = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    modified_at = models.DateTimeField(default=timezone.now)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class LearningLog(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    expire_time = models.DateTimeField(null=True)


class OrderLog(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    cash_spent = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    reward_spent = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    payment_method = models.SmallIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    refunded_at = models.DateTimeField(default=timezone.now)
