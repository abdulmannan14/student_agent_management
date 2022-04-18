from django.urls import path
from Company.views_api.company_register import *
from Company.views_api.get_company_list import *
from Company.views_api.company_update import *
from Company.views_api.company_delete import *

urlpatterns = [
    path('company/register', company_register, name='company-register'),
    path('company/get', get_company_list, name='get-company-list'),
    path('company/update/<int:pk>', company_update, name='company-update'),
    path('company/delete/<int:pk>', company_delete, name='company-delete')
]
