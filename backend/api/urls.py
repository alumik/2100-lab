# pylint: disable=C0103

from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('core/', include('core.urls', namespace='core')),
    path('admin/', include('admins.urls.urls', namespace='admins')),
    path('courses/', include('courses.urls.urls', namespace='courses')),
    path('customers/', include('customers.urls.urls', namespace='customers')),
]
