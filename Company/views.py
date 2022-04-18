import re
from datetime import datetime, timedelta, date
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from limoucloud_backend import decorators as backend_decorators, utils as backend_utils
from django.contrib.auth.models import User
from Vehicle import tables as vehicle_tables, models as vehicle_models, forms as vehicle_forms
from Client import models as client_models, forms as client_forms, tables as client_tables
from Employee import forms as employee_forms, tables as employee_tables, models as employee_models
from Reservation import models as reservation_models, utils as reservation_utils, forms as reservation_forms, \
    tables as reservation_tables
from limoucloud_backend.utils import success_response, failure_response, success_response_fe, failure_response_fe
from . import models as company_models, utils as company_utils, urls as company_urls, forms as company_forms
from Account import utils as account_utils
from Account.models import UserProfile, Configuration
from setting import models as setting_models, forms as setting_forms
from django.db.models import Q
from Home import models as home_models, tables as home_tables
from django.templatetags.static import static


@user_passes_test(backend_decorators._is_manager_or_dispatcher_or_company)
def my_profile(request):
    get_user = request.user
    if request.method == 'POST':
        get_or_edit_user_profile = backend_utils.Get_or_edit_user_profile(request.POST, instance=get_user.userprofile)
        get_or_edit_user = backend_utils.Get_or_edit_user(request.POST, instance=get_user)
        get_or_edit_user_address = backend_utils.Get_or_edit_user_address(request.POST,
                                                                          instance=get_user.userprofile.address)
        if get_or_edit_user_profile.is_valid() and get_or_edit_user.is_valid() and get_or_edit_user_address.is_valid():
            company_utils.saving_user_details(get_or_edit_user, get_or_edit_user_address,
                                              get_or_edit_user_profile)
            return redirect('my-profile-company')
    else:
        get_or_edit_user_profile = backend_utils.Get_or_edit_user_profile(instance=get_user.userprofile)
        get_or_edit_user = backend_utils.Get_or_edit_user(instance=get_user)
        get_or_edit_user_address = backend_utils.Get_or_edit_user_address(instance=get_user.userprofile
                                                                          .address)
        context = {
            "page_title": "My Profile",
            "subtitle": "Here you can edit the profile also",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form1': get_or_edit_user,
            'address_form': get_or_edit_user_address,
            'profile_form': get_or_edit_user_profile,
            'button': 'save',
        }
        return render(request, "dashboard/add_or_edit.html", context)


def index(request):
    today = date.today()
    context = {
        "cards": [
            {
                "title": "Pending Trips",
                "value": '34',
                "icon": "fa-users",
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/PendingTrips.svg"),
            },
            {
                "title": " Today's Trips",
                "value": '45',
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            },
            {
                "title": "Driver Available",
                "value": '34',
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/DriversAvailable.svg"),
            },
            {
                "title": "Trip Paid Today",
                "value": '34',
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsPaidToday.svg"),
            },
            {
                'title': "Tomorrow's Trips",
                "value": '23',
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsTomorrow.svg"),
            },
            {
                "title": "Pending Trips",
                "value": 45,
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/PendingTrips.svg"),
            },
            {
                "title": " Today's Trips",
                "value": 23,
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            },
            {
                "title": "Driver Available",
                "value": 34,
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/DriversAvailable.svg"),
            },
            {
                "title": "Trip Paid Today",
                "value": 34,
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsPaidToday.svg"),
            },
            {
                "title": "Tomorrow's Trips",
                "value": 34,
                "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsTomorrow.svg"),
            },
        ],
        'driver_trips_info': 'driver_trips_info',
        'vehicles_trips_info': 'vehicles_trips_info',
        'graph_year_data': [5333, 3, 1, 4, 1, 6, 2, 6, 6],
        'get_user_role': 'user_role',
        'nav_conf': {
            'active_classes': ['index'],
        },
    }
    return render(request, "dashboard/company/index.html", context)


from Account import forms as account_forms


@user_passes_test(backend_decorators._is_company)
def update_company_overview(request):
    company = request.user.userprofile.companyprofilemodel
    user_form = account_forms.UserForm(request.POST or None, instance=request.user)
    company_form = company_forms.CompanyProfileForm(request.POST or None, instance=company)
    company_address = company_forms.CompanyAddressForm(request.POST or None, instance=company.address)
    if request.method == "POST":
        if user_form.is_valid() and company_form.is_valid() and company_address.is_valid():
            user_form.save()
            address = company_address.save()
            if not company.address:
                company.address = address
                company.save()
            company_form.save()
            messages.success(request, "Information Updated")

    context = {
        "title": "Update Information",
        "page_title": "Update Information",
        "forms": [
            {
                "title": "",
                "form": company_form
            },
            {
                "title": "",
                "form": user_form,
            },

            {
                "title": "",
                "form": company_address,
            },
        ],
        'nav_conf': {
            'active_classes': ['company'],
        },
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
    }
    return render(request, "company/update-info.html", context)


@user_passes_test(backend_decorators._is_company)
def company_overview(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    company_name = company.company_name
    contact_first_name = company.userprofile.user.first_name
    contact_last_name = company.userprofile.user.last_name
    contact_user_name = company.userprofile.user.username
    email = company.userprofile.user.email
    business_phone = company.phone
    secondary_phone = company.secondary_phone
    address = company.address
    date_format = company.date_format
    time_zone = company.timezone
    distance_unit = company.distance_unit
    currency = company.currency
    sales_tax = company.sales_tax

    context = {
        'company_info': 'Company Info',
        'company': company_name,
        'contact_first_Name': contact_first_name,
        'contact_last_name': contact_last_name,
        'contact_user_name': contact_user_name,
        'email': email,
        'business_phone': business_phone,
        'secondary_phone': secondary_phone,
        'address': address,
        'date_format': date_format,
        'time_zone': time_zone,
        'distance_unit': distance_unit,
        'currency': currency,
        'sales_tax': sales_tax,
        'nav_conf': {
            'active_classes': ['company'],
        },
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        # 'button': 'OK'

    }
    return render(request, "company/overview.html", context)


# def accounts(request):
#     today = date.today()
#     request_user = request.user
#     request_user_name = request_user.username
#     user_role = request_user.userprofile.role
#
#     # FOR CLIENTS
#     clients = client_models.PersonalClientProfileModel.objects.filter(
#         company__userprofile__user__username=request_user_name)
#     individual_clients = []
#     corporate_clients = []
#     for client in clients:
#         if client.is_corporate_client == True:
#             corporate_clients.append(client)
#         else:
#             individual_clients.append(client)
#
#     # FOR EMPLOYEES
#     employees = employee_models.EmployeeProfileModel.objects.filter(
#         company__userprofile__user__username=request_user_name)
#
#     # FOR VEHICLE
#
#     vehicles = vehicle_models.Vehicle.objects.filter(company__userprofile__user__username=request_user_name)
#
#     # FOR RESERVATIONS
#     reservation = reservation_models.Reservation.objects.filter(
#         company__userprofile__user__username=request_user_name)
#
#     paid_reservations = reservation_models.Reservation.objects.filter(balance_paid=True, reservation_status='COMPLETED',
#                                                                       pick_up_date__gte=(today - timedelta(days=7)))
#     unpaid_reservations = reservation_models.Reservation.objects.filter(balance_paid=False,
#                                                                         reservation_status='COMPLETED',
#                                                                         pick_up_date__gte=(today - timedelta(days=7)))
#     amount_of_paid_reservations = company_utils.get_sum_of_all_reservation_fares(paid_reservations)
#     amount_of_unpaid_reservations = company_utils.get_sum_of_all_reservation_fares(unpaid_reservations)
#     driver_run_count_true = reservation_models.Reservation.objects.filter(accepted_by_driver=True)
#     driver_run_count_false = reservation_models.Reservation.objects.filter(accepted_by_driver=False)
#     vehicle_run_count_true = vehicle_models.Vehicle.objects.filter(is_on_ride=True)
#     vehicle_run_count_false = vehicle_models.Vehicle.objects.filter(is_on_ride=False)
#     last_month_client = company_utils.get_increment_percentage(clients)
#     corporate_clients = clients.filter(is_corporate_client=True)
#     individual_clients = clients.filter(is_corporate_client=False)
#     last_month_corporate_client = company_utils.get_increment_percentage(corporate_clients)
#     last_month_individual_client = company_utils.get_increment_percentage(individual_clients)
#     last_month_vehicle = company_utils.get_increment_percentage(vehicles)
#     last_month_reservation = company_utils.get_increment_percentage(reservation)
#     last_month_employees = company_utils.get_increment_percentage(employees)
#
#     context = {
#         'total_clients_tag': 'Total No of clients',
#         'total_clients_quantity': len(clients),
#         'total_corporate_clients_tag': 'Corporate clients',
#         'total_individual_clients_tag': 'Individual clients',
#         'corporate_count': len(corporate_clients),
#         'individual_count': len(individual_clients),
#         'total_employees_tag': 'Total employees',
#         'total_employees_quantity': len(employees),
#         'total_vehicles_tag': 'Total vehicles',
#         'total_vehicles_quantity': len(vehicles),
#         'total_reservations_tag': 'Total reservations',
#         'total_reservations_quantity': len(reservation),
#         'driver_run_count_chart': 'Driver Run Count',
#         'vehicle_run_count_chart': 'Vehicle Run Count',
#         'total_marked_paid_reservation_this_week': 'Total Marked PAID reservation this week',
#         'total_marked_not_paid_reservation_this_week': 'Total Marked NOT PAID reservation this week',
#         'number_of_paid_reservations': len(paid_reservations),
#         'number_of_not_paid_reservations': len(unpaid_reservations),
#         'amount_of_paid_reservations': amount_of_paid_reservations,
#         'amount_of_not_paid_reservations': amount_of_unpaid_reservations,
#         'driver_run_count_true': len(driver_run_count_true),
#         'driver_run_count_false': len(driver_run_count_false),
#         'vehicle_run_count_true': len(vehicle_run_count_true),
#         'vehicle_run_count_false': len(vehicle_run_count_false),
#         'get_user_role': user_role,
#         'total_client_increment': f"{last_month_client}%",
#         'total_corporate_client_increment': f"{last_month_corporate_client}%",
#         'total_individual_client_increment': f"{last_month_individual_client}%",
#         'total_vehicle_increment': f"{last_month_vehicle}%",
#         'total_reservation_increment': f"{last_month_reservation}%",
#         'total_emmployees_increment': f"{last_month_employees}%",
#
#     }
#     return render(request, "dashboard/accounts/index.html", context)


"""here are all the views related to  ''employees'' 
   all the work related to employees while remaining
   in the company section will be managed by this"""


@user_passes_test(backend_decorators._is_company_or_manager)
def all_employee(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    employees = company.employeeprofilemodel_set.all()
    # employees = employee_models.EmployeeProfileModel.objects.filter(
    #     company__company_name=company)
    sort = request.GET.get('sort', None)
    if sort:
        employees = employees.order_by(sort)
    table = employee_tables.EmployeeProfileTablesForCompany(employees)
    context = {
        'links': [
            {
                'color_class': 'btn-primary',
                'title': 'New Staff',
                'href': reverse('company-add-employee'),
                # 'icon': 'fa fa-plus'
            },
        ],
        'employee_count': len(employees),
        'page_title': 'Staff',
        'subtitle': 'All the employees are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['employees'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def add_employee(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == "POST":
        form = employee_forms.EmployeeProfileForm(request.POST)
        user_form = employee_forms.UserForm(request.POST)
        get_email = request.POST.get('email')
        address = employee_forms.EmployeeAddressForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            if account_utils._get_user(email=get_email):
                messages.error(request, "sorry a user is already registered with this email")
                return redirect("company-add-employee")
            address_form = address.save()
            user = user_form.save(commit=False)
            password = User.objects.make_random_password(length=10)
            user.set_password(password)
            user = user_form.save()

            employee_role = request.POST.get('title')
            primary_phone = request.POST.get('primary_phone')
            context = {
                'subject': 'Your <strong>{employee_role}</strong> account is created at Limoucloud.'.format(
                    employee_role=employee_role),
                'message': f'Thank you   {user.username} ! your {employee_role} account has been Created at LimouCloud. As you are new to our system so you need to update your password.'
                           f'  Your current password is:{password}',
            }
            account_utils._thread_making(backend_utils.send_email, ["Welcome to LimouCloud", context, user])

            configurations = Configuration.objects.create(dark_mode=False, location=True, notification=True,
                                                          new_trips_notifications=True)
            user_profile = UserProfile.objects.create(user=user, verification_code=account_utils.random_digits(),
                                                      email_verified=True,
                                                      role=employee_role.upper(), phone=primary_phone, step_count=4,
                                                      config=configurations)
            configurations.save()
            user_profile.address = address_form
            user_profile.save()
            employee = form.save(commit=False)
            employee.employee_role = employee_role
            employee.userprofile = user_profile
            employee.company = company

            employee.save()
            messages.success(request, "Employee Is Added Successfully!")
            return redirect("company-all-employees")
        else:
            messages.error(request, "sorry a user is already registered with this username!")
            return redirect("company-add-employee")

    else:
        form = employee_forms.EmployeeProfileForm()
        form1 = employee_forms.EmployeeProfileFormForPosition()
        roles = employee_models.EmployeeRole.objects.filter(company=company)
        form1.fields['title'].choices = [(role.title, role.title) for role in roles]
        user_form = employee_forms.UserForm()
        address = employee_forms.EmployeeAddressForm()

        context = {
            "page_title": "Add Staff:",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            "employee_form": form1,
            "form2": user_form,
            'form_address': address,
            'form_phone_number': form,
            'company_id': company.id,
            'button': 'Save',
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('company-all-employees'),
            'nav_conf': {
                'active_classes': ['employees'],
            },

        }
        return render(request, "dashboard/add_or_edit.html", context)


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def edit_employee(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    employees = get_object_or_404(employee_models.EmployeeProfileModel, pk=pk, company=company)
    if request.method == 'POST':
        form = employee_forms.EmployeeProfileForm(request.POST, instance=employees)
        user_form = employee_forms.UserForm(request.POST, instance=employees.userprofile.user)
        username = request.POST.get('username')
        email = request.POST.get('email')
        if form.is_valid():

            if user_form.has_changed() == True and user_form.data['email'] == employees.userprofile.user.email and \
                    user_form.data['username'] == employees.userprofile.user.username:
                user_form.save()
            if user_form.has_changed() == True and user_form.data['email'] != employees.userprofile.user.email:
                if account_utils._get_user(email=email):
                    messages.error(request, "sorry a user is already registered with this email")
                    return redirect("company-edit-employee", pk=pk)
                user_form.save()
            if user_form.has_changed() == True and user_form.data['username'] != employees.userprofile.user.username:
                if account_utils._get_user(username=username):
                    messages.error(request, "sorry a user is already registered with this username")
                    return redirect("company-edit-employee", pk=pk)
                user_form.save()
            user = user_form.save(commit=False)
            password = request.POST.get('password')
            if password:
                user.set_password(request.POST.get('password'))
            user = user_form.save()
            employee_role = request.POST.get('employee_role')
            primary_phone = request.POST.get('primary_phone')
            UserProfile.objects.filter(user=user).update(role=employee_role, phone=primary_phone)
            employees = form.save(commit=False)
            employees.userprofile.user = user
            employees.save()
            messages.success(request, "Employee Is Edited Successfully!")
            return redirect('company-all-employees')
    else:
        form = employee_forms.EmployeeProfileForm(instance=employees)
        user_form = employee_forms.UserForm(instance=employees.userprofile.user,
                                            initial={"password": ""})
        context = {
            "page_title": "Edit Employee({})".format(employees.full_name),
            "subtitle": "Please enter the suitable information",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'form1': user_form,
            'form2': form,
            'button': "Submit",
            'nav_conf': {
                'active_classes': ['employees'],
            },

        }
        return render(request, "dashboard/add_or_edit.html", context)


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def delete_employee(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    employee = get_object_or_404(employee_models.EmployeeProfileModel, pk=pk, company=company)
    employee_username = employee.userprofile.user.username
    user = get_object_or_404(User, username=employee_username)
    employee.delete()
    user.delete()
    messages.success(request, "Employee Is Deleted Successfully!")
    return redirect('company-all-employees')


@user_passes_test(backend_decorators._is_company_or_manager)
def get_employees_detail(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    employee = get_object_or_404(employee_models.EmployeeProfileModel, pk=pk, company=company)
    table_html = backend_utils._get_details_table(employee, exclude=['userprofile_id', 'id', 'company_id'])
    return JsonResponse(table_html, safe=False)


"""here are all the views related to  ''vehicle'' 
   all the work related to vehicles while remaining
   in the company section will be managed by this"""


@user_passes_test(backend_decorators._is_company_or_manager)
def all_vehicle(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    vehicles = company.vehicle_set.all()
    # vehicles = vehicle_models.Vehicle.objects.filter(company=company)
    sort = request.GET.get('sort', None)
    if sort:
        vehicles = vehicles.order_by(sort)
    table = vehicle_tables.VehicleTableForCompany(vehicles)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Fleet",
                "href": reverse("company-add-vehicle"),
                "icon": "fa fa-plus"
            },
        ],
        'vehicle_count': len(vehicles),
        "page_title": "Fleet",
        "table": table,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def add_vehicle(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == "POST":
        form = vehicle_forms.VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.cleaned_data['all_vehicle_name']
            vehicle_object = vehicle_models.GeneralVehicle.objects.get(name=vehicle)
            vehicel_image = vehicle_object.image
            vin = form.cleaned_data['vin']
            if not vin.isalnum() or vin.isalpha() or vin.isnumeric():
                messages.error(request, "Vin should be Alphanumeric")
                return redirect("company-add-vehicle")
            vehicle = form.save(commit=False)
            vehicle.company = company
            vehicle.image = vehicel_image
            vehicle.save()
            messages.success(request, "Vehicle Is Added Successfully!")
            return redirect("company-all-vehicles")
    else:
        types = setting_models.VehicleType.objects.filter(company=company)
        form = vehicle_forms.VehicleForm()
        vehicles = vehicle_models.GeneralVehicle.objects.filter(Q(company=company) | Q(company=None))
        form.fields['all_vehicle_name'].queryset = vehicles
        form.fields["vehicle_type"].queryset = types

    context = {
        "page_title": "Add Fleet",
        "add_vehicle": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('company-all-vehicles'),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def edit_vehicle(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    vehicle = get_object_or_404(vehicle_models.Vehicle, pk=pk, company=company)
    if request.method == "POST":
        form = vehicle_forms.VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle_name = form.cleaned_data['all_vehicle_name']
            vehicle_object = vehicle_models.GeneralVehicle.objects.get(name=vehicle_name)
            vehicle_image = vehicle_object.image
            vehicle = form.save(commit=False)
            vehicle.image = vehicle_image
            vehicle.save()

            messages.success(request, "Vehicle Is Edited Successfully!")
            return redirect('company-all-vehicles')
    else:
        form = vehicle_forms.VehicleForm(instance=vehicle)
        vehicles = vehicle_models.GeneralVehicle.objects.filter(Q(company=company) | Q(company=None))
        form.fields['all_vehicle_name'].queryset = vehicles
        context = {
            "form1": form,
            "page_title": "Add Vehicles",
            "subtitle": "Here you can add the vehicles",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'button': 'Submit',
            'nav_conf': {
                'active_classes': ['vehicles'],
            },
        }
    return render(request, "dashboard/add_or_edit.html", context)


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def delete_vehicle(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    backend_utils._delete_table_entry(vehicle_models.Vehicle, pk, company=company)
    messages.success(request, "Vehicle is Deleted Successfully!")
    return redirect('company-all-vehicles')


@user_passes_test(backend_decorators._is_company_or_manager)
def get_vehicle_detail(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    vehicle_data = get_object_or_404(vehicle_models.Vehicle, pk=pk, company=company)
    vehicle = vehicle_data.all_vehicle_name.name
    vehicle_type = vehicle_data.vehicle_type
    driver = vehicle_data.driver
    table_html = backend_utils._get_details_table(vehicle_data, vehicle, driver, vehicle_type,
                                                  exclude=['id', 'company_id', 'created_at',
                                                           'updated_at'])
    return JsonResponse(table_html, safe=False)


"""here are all the views related to  ''checklist'' 
   all the work related to checklist while remaining
   in the company section will be managed by this"""


@user_passes_test(backend_decorators._is_company_or_manager)
def get_vehicle_checklist(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    checklist = vehicle_models.Checklist.objects.filter(vehicle=pk, vehicle__company=company)
    sort = request.GET.get('sort', None)
    if sort:
        checklist = checklist.order_by(sort)
    table = vehicle_tables.VehicleChecklistTable(checklist)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Checklist",
                "href": reverse("company-add-vehicle-checklist", kwargs={'pk': pk}),
                "icon": "fa fa-plus"
            },
        ],
        'vehicle_count': len(checklist),
        "page_title": "Checklist",
        "table": table,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def add_vehicle_checklist(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == "POST":
        form1 = vehicle_forms.VehicleChecklistForm(request.POST)
        form2 = vehicle_forms.ChecklistLightForm(request.POST)
        form3 = vehicle_forms.ChecklistBrakesForm(request.POST)
        form4 = vehicle_forms.ChecklistFluidForm(request.POST)
        form5 = vehicle_forms.ChecklistMiscForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            checklist = form1.save(commit=False)
            light = form2.save()
            brake = form3.save()
            fluid = form4.save()
            miscell = form5.save()
            checklist.lights = light
            checklist.brake_and_tyres = brake
            checklist.fluids = fluid
            checklist.misc = miscell
            checklist.save()
            messages.success(request, "Checklist Is Added Successfully!")
            return redirect("company-checklist-vehicle", pk=pk)
    else:
        form1 = vehicle_forms.VehicleChecklistForm()
        drivers = employee_models.EmployeeProfileModel.objects.filter(
            company=request.user.userprofile.companyprofilemodel, employee_role='Driver')
        form1.fields['driver'].queryset = drivers
        form2 = vehicle_forms.ChecklistLightForm()
        form3 = vehicle_forms.ChecklistBrakesForm()
        form4 = vehicle_forms.ChecklistFluidForm()
        form5 = vehicle_forms.ChecklistMiscForm()

        context = {
            "page_title": "Add Checklist",
            'form1_tag': 'Vehicle And Driver',
            "form1": form1,
            'form2_tag': 'Lights',
            "form2": form2,
            'form3_tag': 'Brakes And Tyres',
            "form3": form3,
            'form4_tag': 'Fluids',
            "form4": form4,
            'form5_tag': 'Miscellaneous',
            "form5": form5,
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'button': 'Submit',
            'nav_conf': {
                'active_classes': ['vehicles'],
            },
        }
    return render(request, "dashboard/add_or_edit.html", context)


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def edit_checklist(request, pk):
    checklist = get_object_or_404(vehicle_models.Checklist, id=pk)
    vehicle = vehicle_models.Vehicle.objects.get(id=checklist.vehicle.id)
    if request.method == "POST":
        form1 = vehicle_forms.VehicleChecklistForm(request.POST, instance=checklist)
        form2 = vehicle_forms.ChecklistLightForm(request.POST, instance=checklist.lights)
        form3 = vehicle_forms.ChecklistBrakesForm(request.POST, instance=checklist.brake_and_tyres)
        form4 = vehicle_forms.ChecklistFluidForm(request.POST, instance=checklist.fluids)
        form5 = vehicle_forms.ChecklistMiscForm(request.POST, instance=checklist.misc)
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            checklist_form = form1.save(commit=False)
            lights_form = form2.save()
            brake_and_tyre_form = form3.save()
            fluids_form = form4.save()
            misc_form = form5.save()
            checklist.lights = lights_form
            checklist_form.brake_and_tyres = brake_and_tyre_form
            checklist_form.fluids = fluids_form
            checklist_form.misc = misc_form
            checklist_form.save()

            messages.success(request, "Checklist Is Edited Successfully!")
            return redirect('company-checklist-vehicle', pk=vehicle.id)
    else:
        form1 = vehicle_forms.VehicleChecklistForm(instance=checklist)
        form2 = vehicle_forms.ChecklistLightForm(instance=checklist.lights)
        form3 = vehicle_forms.ChecklistBrakesForm(instance=checklist.brake_and_tyres)
        form4 = vehicle_forms.ChecklistFluidForm(instance=checklist.fluids)
        form5 = vehicle_forms.ChecklistMiscForm(instance=checklist.misc)
        context = {
            'form1_tag': 'Vehicle And Driver',
            "form1": form1,
            'form2_tag': 'Lights',
            "form2": form2,
            'form3_tag': 'Brakes And Tyres',
            "form3": form3,
            'form4_tag': 'Fluids',
            "form4": form4,
            'form5_tag': 'Miscellaneous',
            "form5": form5,
            "page_title": "Edit Checklist",
            "subtitle": "Here you can edit the Checklist",
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'button': 'Submit',
            'nav_conf': {
                'active_classes': ['vehicles'],
            },
        }
    return render(request, "dashboard/add_or_edit.html", context)


# ASK ASIF SIR
# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def delete_checklist(request, pk):
    checklist_details = vehicle_models.Checklist.objects.get(id=pk)
    vehicle = checklist_details.vehicle_id
    backend_utils._delete_checklist_table_entry(vehicle_models.Checklist, pk)
    messages.success(request, "Checklist is Deleted Successfully!")
    return redirect('company-checklist-vehicle', pk=vehicle)


@user_passes_test(backend_decorators._is_company_or_manager)
def get_checklist_detail(request, pk):
    checklist = get_object_or_404(vehicle_models.Checklist, pk=pk)
    # driver = checklist.driver
    vehicle = checklist.vehicle.all_vehicle_name.name
    table_html = backend_utils._get_details_table_checklist(checklist)
    return JsonResponse(table_html, safe=False)


"""here are all the views related to  ''clients'' 
   all the work related to client while remaining
   in the company section will be managed by this"""


@user_passes_test(backend_decorators._is_company_or_manager)
def all_clients(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    clients = company.personalclientprofilemodel_set.all()
    # clients = client_models.PersonalClientProfileModel.objects.filter(company=company)
    clients_list = []
    for client in clients:
        clients_list.append(client)
    context = {
        "button_links": [
            {
                "color_class": "btn-primary",
                "title": "Add Client",
                "log": "log",
                "icon": "fa fa-plus",
            },
        ],
        'count': len(clients),
        "page_title": "Clients",
        'clients_list': clients_list,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        "client_form": 'its an add client form',
        'nav_conf': {
            'active_classes': ['clients'],
        },

    }
    return render(request, "company/client/all_clients.html", context)


def add_client(request, client_type=None):
    if request.method == "POST":
        company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
        if not company.stripepayment_set.values('secret_key').last()['secret_key']:
            return JsonResponse(success_response_fe({"redirect_url": reverse("stripe-Payment")},
                                                    msg="Please first set your stripe public and secret key"))
        client_address = request.POST.get('client_address_latlong', None)
        if not client_address:
            return JsonResponse(failure_response_fe(msg="Please add valid pickup/drop off addresses!"))
        address_split = client_address.split(',')
        address_lat = address_split[0]
        address_lng = address_split[1]
        user_form = client_forms.UserForm(request.POST)
        profile_form = client_forms.PersonalClientProfileForm(request.POST)
        address_form = client_forms.AddressForm(request.POST)
        businessclientprofileform = client_forms.BusinessClientProfileForm(request.POST)
        clients_form = client_forms.PersonalClientProfileForm()
        clientpaymentinfoform = client_forms.ClientPaymentInfoForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid() and address_form.is_valid() and clientpaymentinfoform.is_valid():
            user = user_form.save(commit=False)
            password = User.objects.make_random_password(length=10)
            user.set_password(password)
            user = user_form.save()
            context = {
                'subject': 'Client has been Created Successfully !',
                'message': f' Thank you   <strong>{user.username}</strong> ! your Client account has been Created and active at <a href="https://qa.limoucloud.com/"><strong>LimouCloud</strong></a>. '
                           f'You can Now Log in into <a href="https://qa.limoucloud.com/"><strong>Limoucloud</strong></a> mobile app for client. '
                           f' As you are new to our system so you need to update your password. '
                           f' Your current password is: <strong>{password}</strong> <br> <br>'
                           f'<br> Thankyou!  '
                           f'<br> Limoucloud Team☺', }
            account_utils._thread_making(backend_utils.send_email, ["Welcome to LimouCloud", context, user])
            role = "CLIENT"
            phone_no = profile_form.cleaned_data['primary_phone']
            secondary_phone_no = profile_form.cleaned_data['secondary_phone']
            configurations = Configuration.objects.create(dark_mode=False, location=True, notification=True)
            profile_form.save(commit=False)
            user_profile = UserProfile.objects.create(user=user, verification_code=account_utils.random_digits(),
                                                      email_verified=True, role=role, phone=phone_no,
                                                      config=configurations)
            configurations.save()
            client = clients_form.save(commit=False)
            corporate = None
            if client_type == 1:
                corporate = True
            if client_type == 2:
                corporate = False
            client.is_corporate_client = corporate
            if client_type == 1:
                business = businessclientprofileform.save()
                client.business_client = business
            client.userprofile = user_profile
            client.company = company
            address = address_form.save(commit=False)
            address.latitude = address_lat
            address.longitude = address_lng
            address.save()
            user_profile.address = address
            user_profile.save()
            payment = clientpaymentinfoform.save()
            client.client_payment_info = payment
            client.primary_phone = phone_no
            client.secondary_phone = secondary_phone_no
            client.save()
            if request.POST.get('payment_method') == 'CREDIT CARD':
                add_details = company_utils.add_client_card_details_to_stripe(client, request)
                if add_details is not False:
                    return JsonResponse(success_response_fe({"redirect_url": reverse("company-all-clients")},
                                                            msg='Client created Successfully'))
                else:
                    return JsonResponse(failure_response_fe(msg="Client card not added successfully"))

            return JsonResponse(success_response_fe({"redirect_url": reverse("company-all-clients")},
                                                    msg='Client created Successfully'))

    else:
        user_form = client_forms.UserForm()
        profile_form = client_forms.PersonalClientProfileForm()
        address_form = client_forms.AddressForm()
        businessclientprofileform = client_forms.BusinessClientProfileForm()
        clientpaymentinfoform = client_forms.ClientPaymentInfoForm()
        clients_form = client_forms.PersonalClientProfileForm()
    context = company_utils.get_add_client_context(user_form, clients_form, address_form, clientpaymentinfoform)
    if client_type == 1:
        context2 = company_utils.get_context(businessclientprofileform)
        context['form_steps'].insert(1, context2)
    return render(request, "company/client/create.html", context)


# @login_required
def client_overview(request, id):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    client = get_object_or_404(client_models.PersonalClientProfileModel, id=id, company=company)
    if client.client_payment_info.payment_method=='CREDIT CARD':
        card_details = company_utils._get_client_card_details(company, client)
    corporate = client.is_corporate_client
    if corporate:
        businessclientprofileform = client_forms.EditBusinessClientProfileForm(instance=client.business_client)
    user_form = client_forms.UserForm(instance=client.userprofile.user)
    profile_form = client_forms.PersonalClientProfileForm()
    address_form = client_forms.AddressForm(instance=client.userprofile.address)
    # businessclientprofileform = client_forms.BusinessClientProfileForm()
    clientpaymentinfoform = client_forms.ClientPaymentInfoForm(instance=client.client_payment_info)
    clients_form = client_forms.PersonalClientProfileForm(instance=client)

    context = company_utils.get_client_overview_context(client, user_form, clients_form, address_form,
                                                        clientpaymentinfoform)
    if client.client_payment_info.payment_method == 'CREDIT CARD':
        card_context = {
            'card_details_view': True,
            'card_expiry': card_details[0],
            'card_number': card_details[2],
        }
        context['form_steps'][1]['forms'].insert(3, card_context)

    if corporate:
        context2 = company_utils.get_context(businessclientprofileform)
        context['form_steps'].insert(1, context2)
    return render(request, "company/client/create.html", context)


@user_passes_test(backend_decorators._is_company_or_manager)
def edit_clients(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    client = get_object_or_404(client_models.PersonalClientProfileModel, pk=pk, company=company)
    merchant_account = client.merchant_account if client.merchant_account else client.create_stripe_merchant_account()
    businessclientprofileform = ''
    if request.method == "POST":
        corporate = client.is_corporate_client
        if corporate:
            businessclientprofileform = client_forms.EditBusinessClientProfileForm(request.POST,
                                                                                   instance=client.business_client)
        user_form = client_forms.UserForm(request.POST, instance=client.userprofile.user)
        address_form = client_forms.AddressForm(request.POST, instance=client.userprofile.address)
        # businessclientprofileform = client_forms.BusinessClientProfileForm()
        clientpaymentinfoform = client_forms.ClientPaymentInfoForm(request.POST, instance=client.client_payment_info)
        clients_form = client_forms.PersonalClientProfileForm(request.POST, instance=client)

        username = request.POST.get('username')
        email = request.POST.get('email')
        client_lc_account = client.is_client_active
        client_lc_account = str(client_lc_account)
        client_lc_account = client_lc_account.upper()

        if user_form.is_valid() and address_form.is_valid() and clientpaymentinfoform.is_valid() and clients_form.is_valid():
            client_details = client

            client_phone = clients_form.save()
            new_lc_account_of_client = client_details.is_client_active
            new_lc_account_of_client = new_lc_account_of_client
            if client.is_corporate_client:
                if businessclientprofileform.has_changed() == True and businessclientprofileform.data[
                    'business_name'] != '' and businessclientprofileform.data[
                    'business_phone'] != '' and client.is_corporate_client == True:
                    business = businessclientprofileform.save()
                    client_details.business_client = business
                if client.is_corporate_client == True and businessclientprofileform.data[
                    'business_name'] != '' and businessclientprofileform.data[
                    'business_phone'] != '' and businessclientprofileform.data[
                    'business_email'] != '':
                    client_details.save()

            if address_form.has_changed() == True:
                address = address_form.save()
            if user_form.has_changed() == True and user_form.data['email'] == client.userprofile.user.email and \
                    user_form.data['username'] == client.userprofile.user.username:
                user_details = user_form.save()
            if user_form.has_changed() == True and user_form.data['email'] != client.userprofile.user.email:
                if account_utils._get_user(email=email):
                    messages.error(request, "sorry a user is already registered with this email")
                    return redirect("company-edit-client", pk=pk)
                user_details = user_form.save()
            if user_form.has_changed() == True and user_form.data['username'] != client.userprofile.user.username:
                if account_utils._get_user(username=username):
                    messages.error(request, "sorry a user is already registered with this username")
                    return redirect("company-edit-client", pk=pk)
                user_details = user_form.save()

            messages.success(request, "Client is Edited Successfully!")
            company_utils.send_emails_to_clients(client_lc_account=client_lc_account,
                                                 new_lc_account_of_client=new_lc_account_of_client, client=client)
            if clientpaymentinfoform.has_changed():
                payment = clientpaymentinfoform.save()
                client_details.client_payment_info = payment
            else:
                if request.POST.get('card_number') and request.POST.get('cvv') and request.POST.get(
                        'exp_month') and request.POST.get('card_name') and request.POST.get('exp_year'):
                    add_details = company_utils.add_client_card_details_to_stripe(client, request)
                    if not add_details:
                        return JsonResponse(success_response_fe({"redirect_url": reverse("company-all-clients")},
                                                                msg='Client updated Successfully ! Card details was not correct so card not updated.'))

            return JsonResponse(success_response_fe({"redirect_url": reverse("company-all-clients")},
                                                    msg='Client updated successfully'))
        else:
            return JsonResponse(success_response_fe({"redirect_url": reverse("company-all-clients")},
                                                    msg='Validation Failed'))

    else:
        corporate = client.is_corporate_client
        if corporate:
            businessclientprofileform = client_forms.EditBusinessClientProfileForm(instance=client.business_client)
        user_form = client_forms.UserForm(instance=client.userprofile.user)
        profile_form = client_forms.PersonalClientProfileForm()
        address_form = client_forms.AddressForm(instance=client.userprofile.address)
        clientpaymentinfoform = client_forms.ClientPaymentInfoForm(instance=client.client_payment_info)
        clients_form = client_forms.PersonalClientProfileForm(instance=client)
    context = company_utils.get_edit_client_context(user_form, clients_form, address_form, clientpaymentinfoform)
    if client.client_payment_info.payment_method == 'CREDIT CARD':
        card_details = company_utils._get_client_card_details(company, client)
        card_context = {
            'card_details': True,
            'card_expiry': card_details[0],
            'card_number': card_details[2],
        }
        context['form_steps'][1]['forms'].insert(3, card_context)

    if corporate:
        context2 = company_utils.get_context(businessclientprofileform)
        context['form_steps'].insert(1, context2)
    return render(request, "company/client/create.html", context)


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def delete_clients(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    client = get_object_or_404(client_models.PersonalClientProfileModel, pk=pk, company=company)
    client_username = client.userprofile.user.username
    if client.is_corporate_client:
        client_business_data = client.business_client.id
        client_business_info = get_object_or_404(client_models.BusinessClientProfileModel, id=client_business_data)
        client_business_info.delete()
    try:
        client_payment_data = client.client_payment_info.id
        client_payment_info = get_object_or_404(client_models.ClientPaymentInfoModel, id=client_payment_data)
        client_payment_info.delete()
    except:
        pass
    user = get_object_or_404(User, username=client_username)
    user.delete()
    messages.success(request, "Client is Deleted Successfully!")
    return redirect('company-all-clients')


@user_passes_test(backend_decorators._is_company_or_manager)
def get_client_detail(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    client = get_object_or_404(client_models.PersonalClientProfileModel, pk=pk, company=company)
    table_html = backend_utils._get_details_table(client,
                                                  exclude=["id", "company_id", 'userprofile_id', 'business_client_id',
                                                           'client_payment_info_id', 'created_at', 'updated_at'])
    return JsonResponse(table_html, safe=False)


def check_email_validity(request):
    key = request.GET.get('key', None)
    name = request.GET.get('name', "")
    value = request.GET.get('value', None)
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    username_regex = r'\b[A-Za-z0-9]\b'
    message = ""
    another_user = None
    success = False
    if key:
        another_user = account_utils._get_user(username=key)
    if name.lower() == "email":
        if (re.fullmatch(email_regex, value)):
            already_user = account_utils._get_user(email=value)
            if already_user and already_user != another_user:
                message = "Email already linked to another account"
            else:
                success = True
        else:
            message = "Enter valid email!"
    elif name.lower() == "username":
        if True or (re.fullmatch(username_regex, value)):
            already_user = account_utils._get_user(username=value)
            if already_user and already_user != another_user:
                message = "Username already linked to another account"
            else:
                success = True
        else:
            message = "Enter valid username!"
    else:
        message = ""
    return JsonResponse(success_response(msg="") if success else failure_response(msg=message))


def company_dispatches(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    all_reservations = company.reservation_set.all()
    # all_reservations = reservation_models.Reservation.objects.filter(company=company)
    charge_by = request.POST.get('Charge_By', None)
    status_type = request.POST.get('Status_Type', None)
    pay_by = request.POST.get('Pay_By', None)
    vehicle_type = request.POST.get('Vehicle_Type', None)
    reservations = reservation_utils.get_reservations(all_reservations, company, charge_by=charge_by,
                                                      pay_by=pay_by, status_type=status_type, vehicle_type=vehicle_type)
    types = backend_utils.get_my_company_vehicle_type(company=company)
    form = reservation_forms.DropdownForm()
    form.fields["Vehicle_Type"].choices = types
    table = reservation_tables.Dispatch_table(reservations)
    sort = request.GET.get('sort', None)
    if sort:
        reservations = reservations.order_by(sort)
    context = {
        'page_title': 'Dispatches',
        'subtitle': 'All the Dispatches are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['dispatch'],
        },
    }
    return render(request, 'dashboard/list-entries.html', context)


def company_dispatch_modify(request, id):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    reservation_status = request.GET.get('name')
    reservation = reservation_models.Reservation.objects.get(id=id, company=company)
    reservation.reservation_status = reservation_status
    reservation.save()
    return JsonResponse(success_response(), safe=False)


def feedback(request):
    if request.method == "POST":
        feedback_form = setting_forms.FeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save()
            context = {
                'message': 'Name    : {name} <br>'
                           'Email   : {email} <br>'
                           'Phone   : {phone} <br>'
                           'Message : {message} <br>'.format(name=feedback.full_name, email=feedback.email,
                                                             phone=feedback.phone_number,
                                                             message=feedback.message),
            }
            account_utils._thread_making(backend_utils.send_email,
                                         ['Feedback/{}'.format(feedback.full_name), context, '',
                                          'mannanmaan1425@gmail.com'])
            messages.success(request, 'Feedback sent successfully')
            return redirect('company-feedback')

    else:
        feedback_form = setting_forms.FeedbackForm()
        context = {
            "feedback": feedback_form,
            'header_msg': "We'd love to hear from you",
            'header_small_msg': "Contact us using the form below and we'll get back to you right away",
            'card_msg': "Fill out the form and we'll be in touch as soon as possible",
            'nav_conf': {
                'active_classes': ['feedback'],
            },

        }
    return render(request, "company/feedback.html", context)


def graph_values_generator(request):
    value = request.GET.get('value')


def records(request):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    emails = company.email_set.all()
    # emails = home_models.Email.objects.filter(company=company)
    sort = request.GET.get('sort', None)
    if sort:
        emails = emails.order_by(sort)
    table = home_tables.EmailTableForCompany(emails)
    context = {
        "page_title": "Records",
        "table": table,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['records'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def help(request):
    help_list = []
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    if request.method == 'POST':
        user = request.user
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        context = {
            'message': 'Name    : {name} <br>'
                       'Email   : {email} <br>'
                       'Subject   : {subject} <br>'
                       'Message : {message} <br>'.format(name=user, email=user.email,
                                                         subject=subject,
                                                         message=message),
        }
        account_utils._thread_making(backend_utils.send_email,
                                     ['Help in/{}'.format(subject), context, '',
                                      'mannanmaan1425@gmail.com'])
        message = messages.success(request,
                                   "Thank you for submitting LimouCloud ticket,Help team will get back to you soon!  ")
        return redirect('company-help')
    else:
        help_categorties = home_models.HelpCategory.objects.all()
        for help in help_categorties:
            data = {
                "title": help.name,
            }
            help_list.append(data)

        context = {
            'data': help_list,
            'help_header_tag': 'How can we help you?',
            'nav_conf': {
                'active_classes': ['help'],
            },
        }
    return render(request, "dashboard/company/help.html", context)


def help_modal_data(request):
    user = request.user
    username = user.username
    email = user.email
    data = {
        'username': username,
        'email': email,
    }
    return JsonResponse(success_response(data=data))
