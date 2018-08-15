# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('auth/get-verification-code/', views.get_verification_code, name='get-verification-code'),
    path('auth/authenticate/', views.authenticate, name='authenticate'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/is-authenticated/', views.is_authenticated, name='is-authenticated'),
    path('auth/get-eula/', views.get_eula, name='get-eula'),
    path('auth/delete-customer/', views.delete_customer, name='delete-customer'),
]
