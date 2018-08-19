# pylint: disable=C0103

from django.urls import path

from . import views

app_name = 'admins'

urlpatterns = [
    path('admins/authenticate-admin/', views.authenticate_admin, name='authenticate-admin'),
]
