# pylint: disable=C0103

from django.urls import path, include

app_name = 'admins'

urlpatterns = [
    path('backstage/', include('admins.urls.urls_backstage', namespace='backstage')),
]
