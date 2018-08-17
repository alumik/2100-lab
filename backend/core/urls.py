# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('auth/logout/', views.logout, name='logout'),
    path('auth/is-authenticated/', views.is_authenticated, name='is-authenticated'),
    path('auth/delete-user/', views.delete_user, name='delete-user'),
]
