from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html

from . import models as client_models
import django_tables2 as tables
from Employee import urls as employee_urls
from limoucloud_backend import utils as backend_utils
from Company import urls as company_urls


class PersonalClientProfileTableForCompany(tables.Table):
    Corporate_Account = tables.Column(empty_values=())
    LC_Account = tables.Column(empty_values=())
    actions = tables.Column(empty_values=())
    userprofile = tables.columns.TemplateColumn(template_code=u"""{{record.userprofile.user.get_full_name}}""",
                                                verbose_name="Name")
    primary_phone = tables.columns.TemplateColumn(template_code=u"""{{record.primary_phone}}""", verbose_name="phone")

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here', }
        model = client_models.PersonalClientProfileModel
        fields = ['userprofile', 'userprofile.address', 'primary_phone', 'userprofile.user.email', 'LC_Account',
                  'Corporate_Account']

    def render_Corporate_Account(self, record):
        value = record.userprofile.personalclientprofilemodel.is_corporate_client
        if value == True:
            value = "Yes"
        elif value == False:
            value = "No"
        elif value == None:
            value = "N/A"
        return format_html("{value}".format(
            value=value
        )
        )

    def render_LC_Account(self, record):
        value = record.userprofile.personalclientprofilemodel.is_client_active
        if value == True:
            value = "Yes"
        elif value == False:
            value = "No"
        elif value == None:
            value = "N/A"
        return format_html("{value}".format(
            value=value
        )
        )

    def render_actions(self, value, record):
        return format_html("<a class='btn btn-sm text-success' href='{cards}'><i class='fa fa-credit-card'></i></a>"
                           "<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=record.client_edit_url(),
            delete=backend_utils.delete_action(record.client_delete_url(), record.userprofile),
            detail=backend_utils.detail_action(company_urls.get_detail_client(record.pk), record.userprofile),
            cards=reverse("stripe-client-cards", kwargs={"pk": record.pk})
        )
        )


class PersonalClientProfileTableForCompanyAccountingCustomers(tables.Table):
    Corporate_Account = tables.Column(empty_values=())
    LC_Account = tables.Column(empty_values=())
    actions = tables.Column(empty_values=())
    userprofile = tables.columns.TemplateColumn(template_code=u"""{{record.userprofile.user.get_full_name}}""",
                                                verbose_name="Name")
    primary_phone = tables.columns.TemplateColumn(template_code=u"""{{record.primary_phone}}""", verbose_name="phone")

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here', }
        model = client_models.PersonalClientProfileModel
        fields = ['userprofile', 'userprofile.address', 'primary_phone', 'userprofile.user.email', 'LC_Account',
                  'Corporate_Account']

    def render_Corporate_Account(self, record):
        value = record.userprofile.personalclientprofilemodel.is_corporate_client
        if value == True:
            value = "Yes"
        elif value == False:
            value = "No"
        elif value == None:
            value = "N/A"
        return format_html("{value}".format(
            value=value
        )
        )

    def render_LC_Account(self, record):
        value = record.userprofile.personalclientprofilemodel.is_client_active
        if value == True:
            value = "Yes"
        elif value == False:
            value = "No"
        elif value == None:
            value = "N/A"
        return format_html("{value}".format(
            value=value
        )
        )

    def render_actions(self, record):
        html = render_to_string("dashboard/accounts/sales/customers/tables.html")
        return format_html(html)


class PersonalClientProfileTableForEmployee(tables.Table):
    actions = tables.Column(empty_values=())
    userprofile = tables.columns.TemplateColumn(template_code=u"""{{record.userprofile.user.get_full_name}}""",
                                                verbose_name="Name")
    business_client = tables.columns.TemplateColumn(template_code=u"""{{record.business_client.business_name}}""",
                                                    verbose_name="Business Name")
    client_payment_info = tables.columns.TemplateColumn(
        template_code=u"""{{record.client_payment_info.card_name}}""", verbose_name="Payment Info")
    is_client_active = tables.columns.TemplateColumn(template_code=u"""{{record.is_client_active}}""",
                                                     verbose_name="is_active")
    is_corporate_client = tables.columns.TemplateColumn(template_code=u"""{{record.is_corporate_client}}""",
                                                        verbose_name="is_corporate")
    primary_phone = tables.columns.TemplateColumn(template_code=u"""{{record.primary_phone}}""",
                                                  verbose_name="phone")

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here', }
        model = client_models.PersonalClientProfileModel
        exclude = ['id', "created_at", "updated_at", 'company']

    def render_actions(self, value, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=employee_urls.edit_clients(record.pk),
            delete=backend_utils.delete_action(employee_urls.delete_clients(record.pk), record.userprofile),
            detail=backend_utils.detail_action(employee_urls.get_detail_client(record.pk), record.userprofile)
        )
        )
