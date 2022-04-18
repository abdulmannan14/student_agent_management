from django.urls import path
from .views_api import *

urlpatterns = [
    path('client/register', client_register, name='client-register'),
    path('client/get', get_client, name='client-get'),
    path('client/edit/<int:pk>', update_client, name='client-edit'),
    path('client/delete/<int:pk>', delete_client, name='client-delete')
]
