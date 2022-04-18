from django.urls import path
from .views_api import *

urlpatterns = [
    path('employee/register', employee_register, name='employee-register'),
    path('employee/get', get_employee, name='employee-get'),
    path('employee/edit/<int:pk>', edit_employee, name='employee-update'),
    path('employee/delete/<int:pk>', delete_employee, name='employee-delete')
]
