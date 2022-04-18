import django_tables2 as tables
from django.utils.html import format_html

from limoucloud_backend.utils import delete_action, detail_action
from . import models as employee_models, urls as employee_urls
from Vehicle import models as vehicle_models
from Company import urls as company_urls


class EmployeeProfileTablesForCompany(tables.Table):
    userprofile = tables.columns.TemplateColumn(template_code=u"""{{record.userprofile.user.get_full_name}}""",
                                                verbose_name="Name")
    email = tables.columns.TemplateColumn(template_code=u"""{{record.userprofile.user.email}}""",
                                          verbose_name="email")
    address = tables.columns.TemplateColumn(template_code=u"""{{record.userprofile.address}}""",
                                            verbose_name="address")


    is_active = tables.columns.TemplateColumn(template_code=u"""{{record.is_active}}""",
                                              verbose_name="Work Status")
    actions = tables.Column(empty_values=())


    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = employee_models.EmployeeProfileModel
        exclude = ['id', 'created_at', 'updated_at', 'company', 'secondary_phone', 'Client_Phone_Visible', 'dark_mode']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=company_urls.edit_employee(record.pk),
            delete=delete_action(company_urls.delete_employee(record.pk), record.userprofile),
            detail=detail_action(company_urls.get_detail_employees(record.pk), record.userprofile)

        )
        )


class EmployeeProfileTablesForEmployee(tables.Table):
    actions = tables.Column(empty_values=())
    userprofile = tables.columns.TemplateColumn(template_code=u"""{{record.userprofile.user.get_full_name}}""",
                                                verbose_name="Name")

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = employee_models.EmployeeProfileModel
        exclude = ['id', 'created_at', 'updated_at', 'company']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=employee_urls.edit_employee(record.pk),
            delete=delete_action(employee_urls.delete_employee(record.pk), record.userprofile),
            detail=detail_action(employee_urls.get_detail_employee(record.pk), record.userprofile)
        )
        )
