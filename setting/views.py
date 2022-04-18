from pprint import pprint
from django.contrib import messages
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404

from Accounting.DoubleEntry.utils import add_stripe_chart_of_account, add_sales_tax_chart_of_account, \
    edit_sales_tax_chart_of_account
from Employee import models as employee_models
from limoucloud_backend.utils import success_response
from . import models as setting_models, tables as setting_tables, forms as setting_forms, utils as setting_utils
from Company import models as company_models, utils as company_utils

from limoucloud_backend import utils as backend_utils
from Vehicle import models as vehicle_models
import json
from django.contrib.auth.decorators import user_passes_test
from limoucloud_backend import decorators as backend_decorators, utils as backend_utils
from django.contrib.auth import update_session_auth_hash
from Merchants.stripe import utils as marchant_stripe_utils
import stripe


# Create your views here.


def vehicle_type(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    vehicle_types = company.vehicletype_set.all()
    sort = request.GET.get('sort', None)
    if sort:
        vehicle_types = vehicle_types.order_by(sort)
    table = setting_tables.VehicleTypeTable(vehicle_types)
    context = {
        'links': [
            {
                'color_class': 'btn-primary',
                'title': 'Add Vehicle Type',
                'href': reverse('add-vehicle-type'),
                'icon': 'fa fa-plus'
            },
        ],
        'nav_conf': {
            'active_classes': ['settings', 'vehicle_type'],
            'collapse_class': 'settings',
        },
        'page_title': 'Vehicle Types',
        'subtitle': 'All the Vehicle Types are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),

    }
    return render(request, "dashboard/list-entries.html", context)


def add_vehicle_type(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == 'POST':
        form = setting_forms.VehicleTypeForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_type_name = company.vehicletype_set.filter(
                all_vehicle_type_name=request.POST.get('all_vehicle_type_name'))
            if not vehicle_type_name:
                vehicle_type = form.save(commit=False)
                vehicle_type.company = company
                vehicle_type.save()
                service_types = company.servicetype_set.all()
                for service in service_types:
                    service_price = setting_models.ServicePrice.objects.create(service_type=service,
                                                                               company=company,
                                                                               vehicle_type_id=vehicle_type.id,
                                                                               price_type='Quote')
                messages.success(request, "Vehicle Type is Added Successfully")
                return redirect('vehicle-type')
            messages.error(request, "Vehicle Type is Already Available")
            return redirect('add-vehicle-type')

    else:
        form = setting_forms.VehicleTypeForm()
        vehicle_types = setting_models.GeneralVehicleType.objects.filter(Q(company=company) | Q(company=None))
        form.fields["all_vehicle_type_name"].queryset = vehicle_types
        context = {
            "page_title": "Add Vehicle Type",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'vehicle_type': form,
            'button': "Submit",
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('vehicle-type'),
            'nav_conf': {
                'active_classes': ['settings', 'vehicle_type'],
                'collapse_class': 'settings',
            },

        }
        return render(request, "dashboard/add_or_edit.html", context)


def edit_vehicle_type(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    vehicle_type = get_object_or_404(setting_models.VehicleType, pk=pk, company=company)
    if request.method == 'POST':
        form = setting_forms.VehicleTypeForm(request.POST, request.FILES, instance=vehicle_type)
        if form.is_valid():
            if not setting_models.VehicleType.objects.filter(
                    all_vehicle_type_name=form.cleaned_data['all_vehicle_type_name'], company=company):
                form.save()
                messages.success(request, "Vehicle Type is Edited Successfully")
                return redirect('vehicle-type')
            else:
                messages.error(request, "Vehicle Type is Already available")
                return redirect('add-service-types')
    else:
        form = setting_forms.VehicleTypeForm(instance=vehicle_type)
        vehicle_types = setting_models.GeneralVehicleType.objects.filter(Q(company=company) | Q(company=None))
        form.fields["all_vehicle_type_name"].queryset = vehicle_types
        context = {
            "page_title": "Edit Vehicle Type",
            "subtitle": "Here you can edit vehicle types",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form2': form,
            'button': "Submit",
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('vehicle-type'),
            'nav_conf': {
                'active_classes': ['settings', 'vehicle_type'],
                'collapse_class': 'settings',
            },
        }
        return render(request, "dashboard/add_or_edit.html", context)


def delete_vehicle_type(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    backend_utils._delete_table_entry(setting_models.VehicleType, pk, company)
    messages.success(request, "Vehicle Type is Deleted Successfully")
    return redirect('vehicle-type')


def detail_vehicle_type(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    vehicle_type = get_object_or_404(setting_models.VehicleType, pk=pk, company=company)
    table_html = backend_utils._get_details_table(vehicle_type, exclude=["id", "image", "company_id"])
    return JsonResponse(
        table_html, safe=False
    )


def service_type(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    get_service_types = company.servicetype_set.all()
    sort = request.GET.get('sort', None)
    if sort:
        get_service_types = get_service_types.order_by(sort)
    table = setting_tables.ServicetypeTable(get_service_types)
    context = {
        'links': [
            {
                'color_class': 'btn-primary',
                'title': 'Add Service Type',
                'href': reverse('add-service-types'),
                'icon': 'fa fa-plus'
            },
        ],
        'nav_conf': {
            'active_classes': ['settings', 'service_type'],
            'collapse_class': 'settings',
        },
        'page_title': 'Service  Types',
        'subtitle': 'All the Service Types are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),
    }
    return render(request, "dashboard/list-entries.html", context)


def add_service_type(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == 'POST':
        service_type_id = request.POST.get('all_service_type_name')
        service_type = company.servicetype_set.filter(all_service_type_name_id=service_type_id).first()
        if service_type is None:
            form = setting_forms.ServiceTypeForm(request.POST)
            if form.is_valid():
                service_type = form.save()
                service_type.company = company
                service_type.save()
                vehicle_types = company.vehicletype_set.all()
                # setting_models.VehicleType.objects.filter(company=company)
                for vehicle in vehicle_types:
                    service_price = setting_models.ServicePrice.objects.create(vehicle_type=vehicle,
                                                                               service_type_id=service_type.id,
                                                                               company=company,
                                                                               price_type='Quote')
                    # service_price.save()
                messages.success(request, "Service Type is Added Successfully")
                return redirect('service-types')
        else:
            messages.error(request, "Service Type is Already available")
            return redirect('add-service-types')

    else:
        form = setting_forms.ServiceTypeForm()
        service_types = setting_models.GeneralServiceType.objects.filter(Q(company=company) | Q(company=None))
        form.fields["all_service_type_name"].queryset = service_types
        context = {
            "page_title": "Add Service Type",
            "subtitle": "Here you can add the Service Types",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'service_type': form,
            'button': "Submit",
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('service-types'),
            'nav_conf': {
                'active_classes': ['settings', 'service_type'],
                'collapse_class': 'settings',
            },

        }
        return render(request, "dashboard/add_or_edit.html", context)


def edit_service_type(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    service_type = get_object_or_404(setting_models.ServiceType, pk=pk, company=company)
    if request.method == 'POST':
        form = setting_forms.ServiceTypeForm(request.POST, instance=service_type)
        if form.is_valid():
            if not setting_models.ServiceType.objects.filter(
                    all_service_type_name=form.cleaned_data['all_service_type_name'], company=company):
                form.save()
                messages.success(request, "Service Type is Edited Successfully")
                return redirect('service-types')
            else:
                messages.error(request, "Service Type is Already available")
                return redirect('add-service-types')
    else:
        form = setting_forms.ServiceTypeForm(instance=service_type)
        service_types = setting_models.GeneralServiceType.objects.filter(Q(company=company) | Q(company=None))
        form.fields["all_service_type_name"].queryset = service_types
        context = {
            "page_title": "Edit Service Type",
            "subtitle": "Here you can edit service types",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form2': form,
            'button': "Submit",
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('service-types'),
            'nav_conf': {
                'active_classes': ['settings', 'service_type'],
                'collapse_class': 'settings',
            },
        }
        return render(request, "dashboard/add_or_edit.html", context)


def delete_service_type(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    backend_utils._delete_table_entry(setting_models.ServiceType, pk, company)
    return redirect('service-types')


def detail_service_type(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    service_type = get_object_or_404(setting_models.ServiceType, pk=pk, company=company)
    table_html = backend_utils._get_details_table(service_type)
    return JsonResponse(
        table_html, safe=False
    )


def all_airport(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    get_airport = company.companyairport_set.all()

    sort = request.GET.get('sort', None)
    if sort:
        get_airport = get_airport.order_by(sort)
    table = setting_tables.AirportsTable(get_airport)
    context = {
        'links': [
            {
                'color_class': 'btn-primary',
                'title': 'Add GeneralAirport',
                'href': reverse('add-airports'),
                'icon': 'fa fa-plus'
            },
        ],
        'nav_conf': {
            'active_classes': ['settings', 'airports'],
            'collapse_class': 'settings',
        },
        'page_title': 'Airports',
        'subtitle': 'All the Airports are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),
    }
    return render(request, "dashboard/list-entries.html", context)


def add_airport(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == 'POST':
        form = setting_forms.AirportsForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.company = company
            form.save()
            messages.success(request, "GeneralAirport is Added Successfully")
            return redirect('all-airports')
    else:
        form = setting_forms.AirportsForm()
        context = {
            "page_title": "Add Airports",
            "subtitle": "Here you can add the Service Areas",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form2': form,
            'button': "Submit",
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('all-airports'),
            'nav_conf': {
                'active_classes': ['settings', 'airports'],
                'collapse_class': ['settings', 'airports']
            },

        }
        return render(request, "dashboard/add_or_edit.html", context)


def edit_airport(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    airport = get_object_or_404(setting_models.CompanyAirport, pk=pk, company=company)
    if request.method == 'POST':
        form = setting_forms.AirportsForm(request.POST, instance=airport)
        if form.is_valid():
            form.save()
            messages.success(request, "GeneralAirport is Edited Successfully")
            return redirect('all-airports')
    else:
        form = setting_forms.AirportsForm(instance=airport)
        context = {
            "page_title": "Edit GeneralAirport",
            "subtitle": "Here you can edit GeneralAirport",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form2': form,
            'button': "Submit",
            'nav_conf': {
                'active_classes': ['settings', 'airports'],
                'collapse_class': 'settings',
            },
        }
        return render(request, "dashboard/add_or_edit.html", context)


def delete_airport(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    backend_utils._delete_table_entry(setting_models.CompanyAirport, pk, company)
    messages.success(request, "GeneralAirport is Deleted Successfully")
    return redirect('all-airports')


def detail_airport(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    airport = get_object_or_404(setting_models.CompanyAirport, pk=pk, company=company)
    table_html = backend_utils._get_details_table(airport)
    return JsonResponse(
        table_html, safe=False
    )


def all_service_area(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    service_areas = company.servicearea_set.all()

    sort = request.GET.get('sort', None)
    if sort:
        service_areas = service_areas.order_by(sort)
    table = setting_tables.ServiceAreaTable(service_areas)
    context = {
        'links': [
            {
                'color_class': 'btn-primary',
                'title': 'Add Service area',
                'href': reverse('add-service-areas'),
                'icon': 'fa fa-plus'
            },
        ],
        'nav_conf': {
            'active_classes': ['settings', 'service_areas'],
            'collapse_class': 'settings',
        },
        'page_title': 'Service  Area',
        'subtitle': 'All the Service Area are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),
    }
    return render(request, "dashboard/list-entries.html", context)


def add_service_area(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == 'POST':
        form = setting_forms.ServiceAreaForm(request.POST)
        if form.is_valid():
            service_area = form.save(commit=False)
            service_area.company = company
            service_area.save()
            messages.success(request, "Service Area is Added Successfully")
            return redirect('all-service-areas')
    else:
        form = setting_forms.ServiceAreaForm
        context = {
            "page_title": "Add Service Area",
            "subtitle": "Here you can add the Service Areas",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form2': form,
            'button': "Submit",
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('all-service-areas'),
            'nav_conf': {
                'active_classes': ['settings', 'service_areas'],
                'collapse_class': 'settings',
            },

        }
        return render(request, "dashboard/add_or_edit.html", context)


def edit_service_area(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    service_area = get_object_or_404(setting_models.ServiceArea, pk=pk, company=company)
    if request.method == 'POST':
        form = setting_forms.ServiceAreaForm(request.POST, instance=service_area)
        if form.is_valid():
            form.save()
            messages.success(request, "Service Area is Edited Successfully")
            return redirect('all-service-areas')
    else:
        form = setting_forms.ServiceAreaForm(instance=service_area)
        context = {
            "page_title": "Edit Service Area",
            "subtitle": "Here you can edit service area",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form2': form,
            'button': "Submit",
            'nav_conf': {
                'active_classes': ['settings', 'service_areas'],
                'collapse_class': 'settings',
            },
        }
        return render(request, "dashboard/add_or_edit.html", context)


def delete_service_area(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    backend_utils._delete_table_entry(setting_models.ServiceArea, pk, company)
    messages.success(request, "Service Area is Deleted Successfully")
    return redirect('all-service-areas')


def detail_service_area(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    service_area = get_object_or_404(setting_models.ServiceArea, pk=pk, company=company)
    table_html = backend_utils._get_details_table(service_area)
    return JsonResponse(
        table_html, safe=False
    )


def all_zones_area(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    zone_areas = company.zone_set.all()
    sort = request.GET.get('sort', None)
    if sort:
        zone_areas = zone_areas.order_by(sort)
    table = setting_tables.ZoneAreaTable(zone_areas)
    context = {
        'links': [
            {
                'color_class': 'btn-primary',
                'title': 'Add Zone area',
                'href': reverse('add-zones-areas'),
                'icon': 'fa fa-plus'
            },
        ],
        'nav_conf': {
            'active_classes': ['settings', 'zones_area'],
            'collapse_class': 'settings',
        },
        'page_title': 'Zones Area',
        'subtitle': 'All the Zones Area are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),
    }
    return render(request, "dashboard/list-entries.html", context)


def add_zones_area(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == 'POST':
        form = setting_forms.ZoneAreaForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.company = company
            form.save()
            messages.success(request, "Zone Area is Added Successfully")
            return redirect('all-zones-areas')
    else:
        form = setting_forms.ZoneAreaForm
        context = {
            "page_title": "Add Zones Area",
            "subtitle": "Here you can add the Zones Areas",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form2': form,
            'button': "Submit",
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('all-zones-areas'),
            'nav_conf': {
                'active_classes': ['settings', 'zones_area'],
                'collapse_class': 'settings',
            },

        }
        return render(request, "dashboard/add_or_edit.html", context)


# TODO Continue Refactoring and security from here @Mannan @AK

def edit_zones_area(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    zone_area = get_object_or_404(setting_models.Zone, pk=pk, company=company)
    if request.method == 'POST':
        form = setting_forms.ZoneAreaForm(request.POST, instance=zone_area)
        if form.is_valid():
            form.save()
            messages.success(request, "Zone Area is Edited Successfully")
            return redirect('all-zones-areas')
    else:
        form = setting_forms.ZoneAreaForm(instance=zone_area)
        context = {
            "page_title": "Edit Zone Area",
            "subtitle": "Here you can edit service area",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form2': form,
            'button': "Submit",
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('all-zones-areas'),
            'nav_conf': {
                'active_classes': ['settings', 'zones_area'],
                'collapse_class': 'settings',
            },
        }
        return render(request, "dashboard/add_or_edit.html", context)


def delete_zones_area(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    backend_utils._delete_table_entry(setting_models.Zone, pk, company)
    messages.success(request, "Zone Area is Deleted Successfully")
    return redirect('all-zones-areas')


def detail_zones_area(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    zone_area = get_object_or_404(setting_models.Zone, pk=pk, company=company)
    table_html = backend_utils._get_details_table(zone_area)
    return JsonResponse(
        table_html, safe=False
    )


def all_service_pricing(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    service_price = company.serviceprice_set.all()
    sort = request.GET.get('sort', None)
    if sort:
        service_price = service_price.order_by(sort)
    table = setting_tables.ServicePriceTable(service_price)
    context = {
        'page_title': 'Service  price',
        'nav_conf': {
            'active_classes': ['settings', 'service_pricing'],
            'collapse_class': 'settings',
        },
        'subtitle': 'All the Service prices are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),
    }
    return render(request, "dashboard/list-entries.html", context)


def all_sales_tax(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    sales_tax = company.salestax_set.all()

    sort = request.GET.get('sort', None)
    if sort:
        sales_tax = sales_tax.order_by(sort)
    table = setting_tables.SalesTax(sales_tax)
    context = {
        'links': [
            {
                'color_class': 'btn-primary',
                'title': 'Add Sales Tax',
                'href': reverse('add-sales-tax'),
                'icon': 'fa fa-plus'
            },
        ],
        'nav_conf': {
            'active_classes': ['settings', 'sales_tax'],
            'collapse_class': 'settings',
        },
        'page_title': 'Sales Tax',
        'subtitle': 'All the Sales Taxes are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),
    }
    return render(request, "dashboard/list-entries.html", context)


def add_sales_tax(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == 'POST':
        sales_tax_form = setting_forms.SalesTaxForm(request.POST)
        tax_rate_form = setting_forms.TaxRateFormForAdd(request.POST)
        if sales_tax_form.is_valid() and tax_rate_form.is_valid():
            tax_rate = tax_rate_form.save(commit=False)
            sales_tax = sales_tax_form.save(commit=False)
            sales_tax: setting_models.SalesTax
            sales_tax.company = company
            sales_tax.save()
            tax_rate: setting_models.TaxRate
            tax_rate.sales_tax = sales_tax
            tax_rate.save()

            # Create Accounting Chart of Account
            add_sales_tax_chart_of_account(company, sales_tax)

            messages.success(request, "Sales Tax Added Successfully")
            return redirect('all-sales-tax')
    else:
        sales_tax_form = setting_forms.SalesTaxForm()
        tax_rate_form = setting_forms.TaxRateFormForAdd()
    context = {
        "page_title": "Add Sales Tax",
        "subtitle": "Here you can add the Sales Tax",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'form1': sales_tax_form,
        'form2': tax_rate_form,
        'button': "Submit",
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('all-sales-tax'),
        'nav_conf': {
            'active_classes': ['settings', 'sales_tax'],
            'collapse_class': 'settings',
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


import itertools


def edit_sales_tax(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    sales_tax = get_object_or_404(setting_models.SalesTax, pk=pk, company=company)
    if request.method == 'POST':
        old_sales_tax_name = sales_tax.name
        sales_tax_form = setting_forms.SalesTaxForm(request.POST, instance=sales_tax)
        tax_rate_form = setting_forms.TaxRateFormForEdit(request.POST)
        if sales_tax_form.is_valid() and tax_rate_form.is_valid():

            sales_tax = sales_tax_form.save()

            # Update Accounting Chart of Account
            edit_sales_tax_chart_of_account(company, old_sales_tax_name, new_sales_tax_obj=sales_tax)

            if tax_rate_form.cleaned_data['rate'] and tax_rate_form.cleaned_data['effective_date']:
                tax_rate = tax_rate_form.save(commit=False)
                tax_rate: setting_models.TaxRate
                tax_rate.sales_tax = sales_tax
                tax_rate.save()
                service_price = setting_models.ServicePrice.objects.filter(sales_tax=sales_tax)
                for i in service_price:
                    i.sales_tax_percentage = tax_rate.rate
                    i.save()

            messages.success(request, "Sales Tax is Edited Successfully")
            return redirect('all-sales-tax')
    else:
        sales_tax_form = setting_forms.SalesTaxForm(instance=sales_tax)
        taxes_list = []
        taxes = setting_models.TaxRate.objects.filter(sales_tax=sales_tax)
        for tax in taxes:
            taxes_list.append(tax)

        tax_rate_form = setting_forms.TaxRateFormForEdit()
    context = {
        "page_title": "Edit Sales Tax",
        "subtitle": "Here you can edit Sales Tax",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'form1': sales_tax_form,
        'current_taxes': taxes_list,
        'form2': tax_rate_form,
        'button': "Submit",
        'nav_conf': {
            'active_classes': ['settings', 'sales_tax'],
            'collapse_class': 'settings',
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def delete_sales_tax(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    backend_utils._delete_table_entry(setting_models.SalesTax, pk, company)
    messages.success(request, "Sales Tax Deleted Successfully")
    return redirect('all-sales-tax')


def detail_sales_tax(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    sales_tax = get_object_or_404(setting_models.SalesTax, pk=pk, company=company)
    table_html = backend_utils._get_details_table(sales_tax)
    return JsonResponse(
        table_html, safe=False
    )


def sales_tax_amount(request):
    sales_tax_id = request.GET.get('id', '')
    tax = setting_models.TaxRate.objects.filter(sales_tax=sales_tax_id).last()
    return JsonResponse(success_response(data=tax.rate))


def edit_pricing(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    service_price = get_object_or_404(setting_models.ServicePrice, pk=pk, company=company)
    price_type = request.POST.get('price_type')
    if request.method == 'POST':
        if price_type == "DISTANCE RATE":
            price_per_mile_distance = request.POST.get('price_per_mile_distance', 0)
            form_distance = setting_forms.VehicleTypePriceForDistance(request.POST)
            form = setting_forms.ServicePriceForm(request.POST, instance=service_price)
            if form.is_valid() and form_distance.is_valid():
                distance_form = form_distance.save()
                service_price_obj = form.save(commit=False)
                service_price_obj.distance_rate = distance_form
                service_price_obj.price = "$ {}/mi".format(price_per_mile_distance)
                service_price_obj.save()
                messages.success(request, "Service Pricing is Edited as DISTANCE RATE Successfully")
                return redirect('all-service-pricing')
        elif price_type == "FLAT RATE":
            flat_rate_rate = request.POST.getlist('rate', 0)
            flat_rate_name = request.POST.getlist('service_area', 0)
            airport = request.POST.get('airport', 0)
            form = setting_forms.ServicePriceForm(request.POST, instance=service_price)
            try:
                airport_data = setting_models.AirportToServiceArea.objects.filter(airport=airport,
                                                                                  service_price_row=service_price)
            except:
                airport_data = False
            if airport_data:
                itr = 0
                for i in airport_data:
                    i.rate = flat_rate_rate[itr]
                    i.save()
                    itr += 1

            service_price_obj = form.save(commit=False)
            service_price_obj.price_type = price_type
            service_price_obj.price = "flat rate per service area"
            service_price_obj.save()
            messages.success(request, "Service Pricing is Edited as FLAT RATE Successfully")
            return redirect('all-service-pricing')
        elif price_type == "HOURLY RATE":
            hours = setting_utils.get_or_create_hours(service_price, 24)
            post_hours = request.POST.getlist("hours_")
            i = 0
            for hour in hours:
                hour.rate = post_hours[i]
                hour.save()
                i = i + 1
            minimum_hours = request.POST.get('minimum_hours')
            form = setting_forms.ServicePriceForm(request.POST, instance=service_price)
            service_price_obj = form.save(commit=False)
            service_price_obj.minimum_hours = minimum_hours
            service_price_obj.price = "per hour(min hrs:{})".format(minimum_hours)
            service_price_obj.save()
            messages.success(request, "Service Pricing is Edited as HOURLY RATE Successfully")
            return redirect('all-service-pricing')
        elif price_type == "ZONE TO ZONE FLAT":
            from_zone = request.POST.getlist('from_zone_input', "")
            to_zone = request.POST.getlist('to_zone_input', "")
            price = request.POST.getlist('price_input', "")
            zone_to_zone_form = setting_forms.VehicleTypePriceForZoneToZone(instance=service_price)
            form = setting_forms.ServicePriceForm(request.POST, instance=service_price)
            all_zones = setting_models.Zone.objects.all()
            for i in range(len(from_zone)):
                from_zone1 = all_zones.get(id=from_zone[i])
                to_zone1 = all_zones.get(id=to_zone[i])
                obj = setting_models.ZoneToZone.objects.create(from_zone=from_zone1, to_zone=to_zone1, price=price[i])
                service_price.zone_to_zone_rate.add(obj)
            service_price.price = "Zone To Zone Flat"
            form.price_type = price_type
            form.save()
            service_price.price = "Zone To Zone Flat"
            service_price.save()
            messages.success(request, "Service Pricing is Edited as ZONE TO ZONE FLAT RATE Successfully")
            return redirect('all-service-pricing')
        else:
            form = setting_forms.ServicePriceForm(request.POST, instance=service_price)
            if form.is_valid():
                form.save()
            return redirect('all-service-pricing')
    else:
        form = setting_forms.ServicePriceForm(instance=service_price)
        # sales_tax = setting_forms.SalesTaxFormForPricing()

        context = {
            "page_title": "Edit Service Price",
            "subtitle": "Here you can edit service price",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form2': form,
            # 'form3': sales_tax,
            'button': "Submit",
            "skip_btn": [
                {
                    "href": reverse("all-service-pricing"),
                    "title": "Cancel",
                    "color_class": " btn-danger"
                }
            ],
            'nav_conf': {
                'active_classes': ['settings', 'service_pricing'],
                'collapse_class': 'settings',
            },
        }
        return render(request, "dashboard/company/partials/add_or_edit_col_6.html", context)


def detail_pricing(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    service_price = get_object_or_404(setting_models.ServicePrice, pk=pk, company=company)
    table_html = backend_utils._get_details_table(service_price)
    return JsonResponse(
        table_html, safe=False
    )


def get_airport(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    airport = request.GET.get('airport')
    service_price_id = request.GET.get('service_price_id')
    get_or_create_data = setting_utils.get_or_create_airport(airport, company, service_price_id)
    service_areas = company.servicearea_set.all()
    forms = []
    for service_area in service_areas:
        try:
            rate = setting_models.AirportToServiceArea.objects.get(service_area__name=service_area,
                                                                   service_area__company=company, airport=airport,
                                                                   service_price_row=service_price_id)
            rate = rate.rate
        except:
            rate = 0
        forms.append({
            "form": setting_forms.FlatRateForm(initial={"service_area": service_area, "rate": rate}),
            "name": service_area.name
        })
    context = {
        "forms": forms,
    }
    html = render_to_string("dashboard/settings/flat_rate_form.html", context, request)
    return JsonResponse(success_response(data=html), safe=False)


def get_price_basis(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    instance_id = request.GET.get("id")
    service_price = get_object_or_404(setting_models.ServicePrice, pk=instance_id, company=company)
    fare_type = request.GET.get('type', '')
    if fare_type == 'FLAT RATE':

        form_field = setting_forms.VehicleTypePriceForFlatRate()
        context = {
            'form_field': form_field,
            'service_price_id': service_price.id,
            'nav_conf': {
                'active_classes': ['settings', 'service_pricing'],
                'collapse_class': 'settings',
            },
        }
        html = render_to_string("dashboard/settings/flat_rate_form.html", context, request)
        return JsonResponse(success_response(data=html), safe=False)
    # TO ASK SIR ASIF
    elif fare_type == 'ZONE TO ZONE FLAT':
        zones = service_price.zone_to_zone_rate.all()
        zone_form = setting_forms.VehicleTypePriceForZoneToZone(instance=service_price)
        context = {
            'dict_zone': zones,
            'zone_form': zone_form,
            'nav_conf': {
                'active_classes': ['settings', 'service_pricing'],
                'collapse_class': 'settings',
            },
        }
    elif fare_type == 'DISTANCE RATE':
        distance_form = setting_forms.VehicleTypePriceForDistance(instance=service_price.distance_rate)
        context = {
            'distance_form': distance_form,
            'nav_conf': {
                'active_classes': ['settings', 'service_pricing'],
                'collapse_class': 'settings',
            },
        }
    elif fare_type == 'HOURLY RATE':
        hours = setting_utils.get_or_create_hours(service_price, 24)
        i = 1
        dict_hour = []
        for hr in hours:
            dict_hour.append({
                'hour': i,
                'rate': hr.rate,

            })
            i = i + 1
        minimum_hour_form = setting_forms.ServicePriceFormForMinimumHour(instance=service_price)
        hour_range = setting_utils.get_hour_range()

        context = {
            'form1': minimum_hour_form,
            'dict_hour': dict_hour,
            'ranger': hour_range,
            'nav_conf': {
                'active_classes': ['settings', 'service_pricing'],
                'collapse_class': 'settings',
            },
        }
        html = render_to_string("dashboard/type_form.html", context, request)
        return JsonResponse(success_response(data=html), safe=False)

    html = render_to_string("dashboard/type_form.html", context, request)
    return JsonResponse(success_response(data=html), safe=False)


def delete_zone_to_zone(request):
    id = request.GET.get('to_zone', '')
    # from_zone = request.GET.get('from_zone')
    # to_zone = request.GET.get('to_zone')
    try:
        zone = setting_models.ZoneToZone.objects.get(id=id).delete()
        messages.success(request, "Zone To Zone is Deleted  Successfully")
        return JsonResponse("found and deleted ", safe=False)
    except:
        return JsonResponse("ok", safe=False)


def add_new_vehicle_type_company(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    vehicle_type = request.GET.get('type', "").title()
    check = setting_models.GeneralVehicleType.objects.filter(name=vehicle_type)
    if check:
        messages.error(request, "Already Available")
        return JsonResponse(True, safe=False)
    else:
        setting_models.GeneralVehicleType.objects.create(name=vehicle_type, company=company)
        messages.success(request, "Added Successfully")
        return JsonResponse(True, safe=False)


def add_new_service_type_company(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    service_type = request.GET.get('type', '').title()
    check = setting_models.GeneralServiceType.objects.filter(name=service_type)
    if check:
        messages.error(request, "Already Available")
        return JsonResponse(True, safe=False)
    else:
        setting_models.GeneralServiceType.objects.create(name=service_type, company=company)
        messages.success(request, "Added Successfully")
        return JsonResponse(True, safe=False)


def add_new_vehicle_company(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    vehicle = request.GET.get('type', '').title()
    check = vehicle_models.GeneralVehicle.objects.filter(name=vehicle)
    if check:
        messages.error(request, "Already Available")
        return JsonResponse(True, safe=False)
    else:
        vehicle_models.GeneralVehicle.objects.create(name=vehicle, company=company)
        messages.success(request, "Added Successfully")
        return JsonResponse(True, safe=False)


def add_new_position_company(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    position = request.GET.get('type').title()
    check = employee_models.EmployeeRole.objects.filter(title=position, company=company)
    if check:
        messages.error(request, "Already Available")
        return JsonResponse(True, safe=False)
    else:
        # company = request.GET.get('company')
        position = position.capitalize()
        # company = int(company)
        employee_models.EmployeeRole.objects.create(title=position, company=company)
        messages.success(request, "Added Successfully")
        return JsonResponse(True, safe=False)


def StripePayment(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    stripe_payment = setting_models.StripePayment.objects.get_or_create(company=company)[0]
    if request.method == 'POST':
        form = setting_forms.PaymentsForm(request.POST, instance=stripe_payment)
        if form.is_valid():
            stripe.api_key = form.cleaned_data['secret_key']
            try:
                stripe.Account.retrieve()['id']
            except:
                messages.error(request, "Provided Secret key doesn't belong to any Stripe Account")
                return redirect('stripe-Payment')
            if company.stripepayment_set.last().account_id:
                if company.stripepayment_set.last().account_id == stripe.Account.retrieve()['id']:
                    stripe_obj = form.save()
                else:
                    messages.error(request, "For the time being you can't change Stripe account")
                    return redirect('stripe-Payment')
            else:
                stripe_obj = form.save(commit=False)
                stripe_obj.account_id = stripe.Account.retrieve()['id']
                stripe_obj.save()
                add_stripe_chart_of_account(company=company, account_id=stripe_obj.account_id)
            messages.success(request, "Payment is added successfully")
            return redirect('stripe-Payment')
        else:
            messages.success(request, "Form is not valid")
            return redirect('stripe-Payment')
    else:
        form = setting_forms.PaymentsForm(instance=stripe_payment)
        context = {
            'nav_conf': {
                'active_classes': ['settings', 'stripe'],
                'collapse_class': 'settings',
            },
            "page_title": "Stripe Account",
            "subtitle": "Here you can configure stripe account integration.",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form1': form,
            'button': "Submit"
        }
    return render(request, "dashboard/add_or_edit.html", context)


def Choosepayment(request):
    context = {
        'nav_conf': {
            'active_classes': ['settings', 'payment'],
            'collapse_class': 'settings',
        },
    }
    return render(request, "dashboard/company/partials/add_or_edit_col_6.html", context)


def company_settings(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    dates = setting_utils._get_company_dates(company)
    company_card_details = setting_utils._get_company_card_details(company)
    context = {
        'company': company,
        'company_last_payment': "{}".format(dates[0]),
        'company_due_payment': dates[1],
        'company_card_details': company_card_details[0],
        'card_number': company_card_details[2],
        'member_since': dates[2],
        'slug': 'Account',
        'page_title': 'Settings',
        'nav_conf': {
            'active_classes': ['company-settings'],

        },
    }
    return render(request, "dashboard/settings/company-settings.html", context)


def company_settings_account(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    packages = company_models.Package.objects.all()
    company_card_details = setting_utils._get_company_card_details(company)
    context = {
        'packages': packages,
        'company_card_details': str(company_card_details[0]),
        'card_number': company_card_details[2],
        'slug': 'Account Detail',
        'page_title': 'Settings',
        'nav_conf': {
            'active_classes': ['company-settings'],

        },

    }
    return render(request, "dashboard/settings/company-settings.html", context)


def company_settings_billing(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    company_card_details = setting_utils._get_company_card_details(company)
    type = f"{company_card_details[1]} ending in: {company_card_details[0]}"
    card_number = company_card_details[2]

    context = {
        'company': company,
        'type': type,
        'card_number': card_number,
        'slug': 'Billing',
        'page_title': 'Settings',
        'nav_conf': {
            'active_classes': ['company-settings'],

        },
    }
    return render(request, "dashboard/settings/company-settings.html", context)


@user_passes_test(backend_decorators._is_company_or_manager)
def company_settings_change_password(request):
    if request.method == 'POST':
        current_password = request.POST['currentpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']
        check_current_pass = backend_utils.check_current_pass(request.user, current_password)
        if check_current_pass:
            check_pass = backend_utils.check_password_matches(new_password, confirm_password)
            if check_pass:
                change_password = backend_utils.change_password(request.user, new_password)
                if change_password:
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Password Changed Successfully')
                    return redirect('company-settings-change-password')
                else:
                    return redirect('company-settings-change-password')
            else:
                messages.error(request, 'New password and confirm password doesn\'t matched')
                return redirect('company-settings-change-password')
        else:
            messages.error(request, 'Current password is incorrect')
            return redirect('company-settings-change-password')
    else:
        context = {
            'slug': 'Change Password',
            'page_title': 'Settings',
            'nav_conf': {
                'active_classes': ['company-settings'],

            },
        }
    return render(request, "dashboard/settings/company-settings.html", context)


def company_settings_contact_support(request):
    context = {
        'slug': 'Contact Support',
        'page_title': 'Settings',
        'nav_conf': {
            'active_classes': ['company-settings'],

        },
    }
    return render(request, "dashboard/settings/company-settings.html", context)


def package_payment_proceed(request):
    slug = request.GET.get('slug')
    slug_obj = company_models.Package.objects.get(slug=slug)
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    create_payment_intent = marchant_stripe_utils.create_payment_intent(company.merchant_account.stripe_id,
                                                                        amount=int(slug_obj.price))

    if create_payment_intent:
        company.company_package.package = slug_obj
        company.company_package.save()
        company.company_package.renew()
    messages.success(request, "Successfully Subscribed")
    return redirect('company-settings')
