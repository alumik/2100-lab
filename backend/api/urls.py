# pylint: disable=C0103

from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('core/', include('core.urls', namespace='core')),
    path('courses/', include('courses.urls', namespace='courses')),
    path('customers/', include('customers.urls', namespace='customers')),
]
