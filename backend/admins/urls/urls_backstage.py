# pylint: disable=C0103, E0401

from django.urls import path

from admins.views import views_backstage

app_name = 'admins'

urlpatterns = [
    path(
        'auth/authenticate-admin/',
        views_backstage.authenticate_admin,
        name='authenticate-admin'
    ),
    path(
        'admin-management/get-admin-list/',
        views_backstage.get_admin_list,
        name='get-admin-list'
    ),
]
