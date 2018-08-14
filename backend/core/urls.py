# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('auth/get_verification_code/', views.get_verification_code, name='get_verification_code'),
    path('auth/authenticate/', views.authenticate, name='authenticate'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/is_authenticated/', views.is_authenticated, name='is_authenticated'),
    path('auth/get_eula/', views.get_eula, name='get_eula'),
]
