from django.urls import path
from .views_api import *

urlpatterns = [
    path('vehicle/register', vehicle_register, name='vehicle-register'),
    path('vehicle/get/all', get_vehicle, name='get-vehicle'),
    path('vehicle/edit/<int:pk>', edit_vehicle, name='edit-vehicle'),
    path('vehicle/delete/<int:pk>', vehicle_delete, name='vehicle-delete')
]