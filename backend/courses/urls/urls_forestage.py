# pylint: disable=C0103, E0401

from django.urls import path

from courses.views import views_forestage

app_name = 'courses'

urlpatterns = [
    path(
        'main/get-heroes/',
        views_forestage.get_heroes,
        name='get-heroes'
    ),
    path(
        'course/get-recent-courses/',
        views_forestage.get_recent_courses,
        name='get-recent-courses'
    ),
    path(
        'course/get-course-list/',
        views_forestage.get_course_list,
        name='get-course-list'
    ),
    path(
        'course/get-course-detail/',
        views_forestage.get_course_detail,
        name='get-course-detail'
    ),
    path(
        'course/up-vote-course/',
        views_forestage.up_vote_course,
        name='up-vote-course'
    ),
    path(
        'course/buy-course/',
        views_forestage.buy_course,
        name='buy-course'
    ),
    path(
        'play/get-course-assets/',
        views_forestage.get_course_assets,
        name='get-course-assets'
    ),
    path(
        'play/get-course-comments/',
        views_forestage.get_course_comments,
        name='get-course-comments'
    ),
    path(
        'play/delete-comment/',
        views_forestage.delete_comment,
        name='delete-comment'
    ),
    path(
        'play/up-vote-comment/',
        views_forestage.up_vote_comment,
        name='up-vote-comment'
    ),
    path(
        'play/down-vote-comment/',
        views_forestage.down_vote_comment,
        name='down-vote-comment'
    ),
    path(
        'play/add-comment/',
        views_forestage.add_comment,
        name='add-comment'
    ),
    path(
        'play/save-learning-log/',
        views_forestage.save_learning_log,
        name='save-learning-log'
    ),
]
