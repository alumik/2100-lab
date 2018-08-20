# pylint: disable=C0103

from django.urls import path, include

app_name = 'customers'

urlpatterns = [
    path('forestage/', include('customers.urls.urls_forestage', namespace='forestage')),
]
