"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html

from Vehicle import models as vehicle_models
from limoucloud_backend.utils import delete_action
from Company import urls as company_urls
from Employee import urls as employee_urls
from limoucloud_backend import utils as backend_utils
# Vehicle Table For Company
class VehicleTableForCompany(tables.Table):
    photo = tables.Column(empty_values=())
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = vehicle_models.Vehicle
        fields=['all_vehicle_name','year','make','model_name','vehicle_type','vehicle_number']
        exclude = ['image',]

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}"
                           "<a class='btn btn-sm text-primary' href='{checklist}'><i class='fa fa-list'></i></a>".format(
            update=company_urls.edit_vehicle(record.pk),
            delete=delete_action(company_urls.delete_vehicle(record.pk), record.all_vehicle_name),
            detail=backend_utils.detail_action(company_urls.get_detail_vehicle(record.pk), record.all_vehicle_name),
            checklist=company_urls.get_checklist_vehicle(record.pk)

        )
        )
    def render_photo(self, record):
        image_link = "/staticfiles/assets/img/no_image.png"
        if record.image:
            image_link = record.image.url
        return format_html("""
        <img height="70px" src='{}'/>
        """.format(image_link))


# Vehicle Table For Employee
class VehicleTableForEmployee(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = vehicle_models.Vehicle
        exclude = ["id", "created_at", "updated_at", 'plate_number', 'insurance_company', 'tabs_expiration_date',
                   'inspection_expiration_date', 'company']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=employee_urls.edit_vehicle(record.pk),
            delete=delete_action(employee_urls.delete_vehicle(record.pk), record.name),
            detail = backend_utils.detail_action(employee_urls.get_detail_vehicle(record.pk), record.name)
        )
        )
class VehicleChecklistTable(tables.Table):
    actions = tables.Column(empty_values=())
    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = vehicle_models.Checklist
        fields= ['vehicle','driver','created_at']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=company_urls.edit_checklist(record.pk),
            delete=delete_action(company_urls.delete_checklist(record.pk), record.vehicle),
            detail=backend_utils.detail_action(company_urls.get_detail_checklist(record.pk), record.vehicle),

        )
        )