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
    path(
        'admin-management/get-admin-detail/',
        views_backstage.get_admin_detail,
        name='get-admin-detail'
    ),
    path(
        'admin-management/change-admin-username/',
        views_backstage.change_admin_username,
        name='change-admin-username'
    ),
    path(
        'admin-management/change-admin-password/',
        views_backstage.change_admin_password,
        name='change-admin-password'
    ),
    path(
        'admin-management/delete-admin/',
        views_backstage.delete_admin,
        name='delete-admin'
    ),
    path(
        'admin-management/add-admin/',
        views_backstage.add_admin,
        name='add-admin'
    ),
    path(
        'admin-management/change-admin-groups/',
        views_backstage.change_admin_groups,
        name='change-admin-groups'
    ),
    path(
        'log-management/get-admin-log/',
        views_backstage.get_admin_log,
        name='get-admin-log'
    ),
]
