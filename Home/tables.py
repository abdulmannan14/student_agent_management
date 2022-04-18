import django_tables2 as tables
from django.utils.html import format_html

from Vehicle import models as vehicle_models
from limoucloud_backend.utils import delete_action
from Company import urls as company_urls
from Employee import urls as employee_urls
from limoucloud_backend import utils as backend_utils
from Home import models as home_models


# email Table For Company
class EmailTableForCompany(tables.Table):
    reservation = tables.Column(verbose_name='Reservation #')
    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = home_models.Email
        # fields =
        exclude = ['id','company', ]
