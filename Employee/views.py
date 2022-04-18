from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.response import Response

from Account import models as account_models
from Account.models import UserProfile
from Account.utils import random_digits
from . import models as employee_models, tables as employee_tables, forms as employee_forms
from limoucloud_backend import decorators as backend_decorators, utils as backend_utils
from Client import models as client_models, tables as client_tables, forms as client_forms
from Reservation import models as reservation_models
from Vehicle import tables as vehicle_tables, forms as vehicle_forms, models as vehicle_models


# MY_PROFILE


def change_pass(request):
    request_user = request.user
    user_role = request_user.userprofile.role
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
                    if user_role == 'MANAGER':
                        messages.success(request, 'Password Changed Successfully ')
                        return redirect('manager-index')
                    else:
                        messages.success(request, 'Password Changed Successfully ')
                        return redirect('dispatcher-index')
                else:
                    return redirect('change-password-employee')
            else:
                messages.error(request, 'New password and confirm password doesn\'t matched.')
                return redirect('change-password-employee')
        else:
            messages.error(request, 'Current password is incorrect.')
            return redirect('change-password-employee')

    else:
        context = {
            'nav_bar': render_to_string("dashboard/company/manager/partials/nav.html")
        }
        return render(request, 'dashboard/changepassword.html', context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher_or_company)
def my_profile(request):
    user = request.user
    if request.method == 'POST':
        get_or_edit_user_profile = backend_utils.Get_or_edit_user_profile(request.POST, instance=user.userprofile)
        get_or_edit_user = backend_utils.Get_or_edit_user(request.POST, instance=user)
        get_or_edit_user_address = backend_utils.Get_or_edit_user_address(request.POST,
                                                                          instance=user.userprofile.address)
        if get_or_edit_user_profile.is_valid() and get_or_edit_user.is_valid() and get_or_edit_user_address.is_valid():
            user = get_or_edit_user.save()
            address = get_or_edit_user_address.save()
            user_details = get_or_edit_user_profile.save(commit=False)
            user_details.user = user
            user_details.address = address
            user_details.save()
            return redirect('my-profile')
    else:
        get_or_edit_user_profile = backend_utils.Get_or_edit_user_profile(instance=user.userprofile)
        get_or_edit_user = backend_utils.Get_or_edit_user(instance=user)
        get_or_edit_user_address = backend_utils.Get_or_edit_user_address(instance=user.userprofile
                                                                          .address)
        context = {
            "page_title": "edit Profile",
            "subtitle": "Here you can edit the profile",
            "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html"),
            'form1': get_or_edit_user,
            'form2': get_or_edit_user_address,
            'form3': get_or_edit_user_profile
        }
        return render(request, "dashboard/add_or_edit.html", context)


##EMPLOYEE_INDEX
@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def index_manager(request):
    request_user = request.user
    request_user_name = request_user.username
    company = employee_models.EmployeeProfileModel.objects.get(userprofile__user__username=request_user_name)
    user_role = request_user.userprofile.role
    if user_role == "DISPATCHER":
        return redirect('dispatcher-index')
    # FOR CLIENTS
    clients = client_models.PersonalClientProfileModel.objects.filter(
        company=company.company)
    individual_clients = []
    corporate_clients = []
    for client in clients:
        if client.is_corporate_client == True:
            corporate_clients.append(client)
        else:
            individual_clients.append(client)

    # FOR EMPLOYEES
    employees = employee_models.EmployeeProfileModel.objects.filter(
        company=company.company)

    # FOR VEHICLE
    vehicles = vehicle_models.Vehicle.objects.filter(company=company.company)

    # FOR RESERVATIONS
    reservation = reservation_models.Reservation.objects.filter(
        company=company.company)
    contect = {
        'total_clients_tag': 'Total No of clients',
        'total_clients_quantity': len(clients),
        'total_corporate_clients_tag': 'Corporate clients',
        'total_individual_clients_tag': 'Individual clients',
        'corporate_count': len(corporate_clients),
        'individual_count': len(individual_clients),
        'total_employees_tag': 'Total employees',
        'total_employees_quantity': len(employees),
        'total_vehicles_tag': 'Total vehicles',
        'total_vehicles_quantity': len(vehicles),
        'total_reservations_tag': 'Total reservations',
        'total_reservations_quantity': len(reservation),
        'driver_run_count_chart': 'Driver Run Count',
        'vehicle_run_count_chart': 'Vehicle Run Count',
        'total_marked_paid_reservation_this_week': 'Total Marked PAID reservation this week',
        'total_marked_not_paid_reservation_this_week': 'Total Marked NOT PAID reservation this week',
        'number_of_paid_reservations': 352,
        'number_of_not_paid_reservations': 2,
        'amount_of_paid_reservations': 12352,
        'amount_of_not_paid_reservations': 23,
        'driver_run_count': 3,
        'total_drivers': 100,
        'vehicle_run_count': 3,
        'total_vehicle': 100,
        'user_role':user_role

    }
    return render(request, "dashboard/company/manager/index.html", contect)


@user_passes_test(backend_decorators._is_employee_dispatcher)
def index_dispatcher(request):
    request_user = request.user
    request_user_name = request_user.username
    company = employee_models.EmployeeProfileModel.objects.get(userprofile__user__username=request_user_name)
    user_role = request_user.userprofile.role
    # FOR CLIENTS
    clients = client_models.PersonalClientProfileModel.objects.filter(
        company=company.company)
    individual_clients = []
    corporate_clients = []
    for client in clients:
        if client.is_corporate_client == True:
            corporate_clients.append(client)
        else:
            individual_clients.append(client)

    # FOR EMPLOYEES
    employees = employee_models.EmployeeProfileModel.objects.filter(
        company=company.company)

    # FOR VEHICLE
    vehicles = vehicle_models.Vehicle.objects.filter(company=company.company)

    # FOR RESERVATIONS
    reservation = reservation_models.Reservation.objects.filter(
        company=company.company)
    contect = {
        'total_clients_tag': 'Total No of clients',
        'total_clients_quantity': len(clients),
        'total_corporate_clients_tag': 'Corporate clients',
        'total_individual_clients_tag': 'Individual clients',
        'corporate_count': len(corporate_clients),
        'individual_count': len(individual_clients),
        'total_employees_tag': 'Total employees',
        'total_employees_quantity': len(employees),
        'total_vehicles_tag': 'Total vehicles',
        'total_vehicles_quantity': len(vehicles),
        'total_reservations_tag': 'Total reservations',
        'total_reservations_quantity': len(reservation),
        'driver_run_count_chart': 'Driver Run Count',
        'vehicle_run_count_chart': 'Vehicle Run Count',
        'total_marked_paid_reservation_this_week': 'Total Marked PAID reservation this week',
        'total_marked_not_paid_reservation_this_week': 'Total Marked NOT PAID reservation this week',
        'number_of_paid_reservations': 352,
        'number_of_not_paid_reservations': 2,
        'amount_of_paid_reservations': 12352,
        'amount_of_not_paid_reservations': 23,
        'driver_run_count': 3,
        'total_drivers': 100,
        'vehicle_run_count': 3,
        'total_vehicle': 100,
        'user_role': user_role

    }
    return render(request, "dashboard/company/dispatcher/index.html", contect)


"""here are all the views related to  ''employees'' 
   all the work related to ''employees'' while remaining
   in the employee section will be managed by this"""


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def all_employee(request):
    request_user = request.user
    request_user_name = request_user.username
    company = employee_models.EmployeeProfileModel.objects.get(userprofile__user__username=request_user_name)
    employees = employee_models.EmployeeProfileModel.objects.filter(company=company.company)
    sort = request.GET.get('sort', None)
    if sort:
        employees = employees.order_by(sort)
    table = employee_tables.EmployeeProfileTablesForEmployee(employees)
    context = {
        'links': [
            {
                'color_class': 'btn-primary',
                'title': 'Add Employee',
                'href': reverse('employee-add-employee'),
                'icon': 'fa fa-plus'
            },
        ],
        'employee_count': len(employees),
        'page_title': 'Employees',
        'subtitle': 'All the employees are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/manager/partials/nav.html")
    }
    return render(request, "dashboard/list-entries.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def add_employee(request):
    if request.method == "POST":
        user: User = request.user
        company = user.userprofile.companyprofilemodel
        form = employee_forms.EmployeeProfileForm(request.POST)
        user_form = employee_forms.UserForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user = user_form.save()
            employee_role = request.POST.get('employee_role')
            primary_phone = request.POST.get('primary_phone')
            user_profile = UserProfile.objects.create(user=user, verification_code=random_digits(), email_verified=True,
                                                      role=employee_role, phone=primary_phone, step_count=4)
            user_profile.save()
            employee: employee_models.EmployeeProfileModel = form.save(commit=False)
            employee.userprofile = user_profile
            employee.company = company
            employee = employee.save()
            return redirect("employee-all-employees")
    else:
        form = employee_forms.EmployeeProfileForm()
        user_form = employee_forms.UserForm()
        context = {
            "page_title": "Add Employees",
            "subtitle": "Here you can add the employees",
            "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html"),
            "form1": user_form,
            'form2': form,
            'button': 'Submit',
        }
        return render(request, "dashboard/add_or_edit.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def edit_employee(request, pk):
    employees = get_object_or_404(employee_models.EmployeeProfileModel, pk=pk)
    if request.method == 'POST':
        form = employee_forms.EmployeeProfileForm(request.POST, instance=employees)
        user_form = employee_forms.UserForm(request.POST, instance=employees.userprofile.user)
        if form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user = user_form.save()
            employee_role = request.POST.get('employee_role')
            primary_phone = request.POST.get('primary_phone')
            user_profile = UserProfile.objects.filter(user=user).update(role=employee_role, phone=primary_phone)
            employees = form.save(commit=False)
            employees.userprofile.user = user
            employees.save()
            return redirect('employee-all-employees')
    else:
        form = employee_forms.EmployeeProfileForm(instance=employees)
        user_form = employee_forms.UserForm(instance=employees.userprofile.user, initial={"password": " "})

        context = {
            "page_title": "Edit Employee({})".format(employees.full_name),
            "subtitle": "Enter the details",
            "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html"),
            'form1': user_form,
            'form2': form,
            'button': 'Submit',
        }
        return render(request, "dashboard/add_or_edit.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def delete_employee(request, pk):
    employee = get_object_or_404(employee_models.EmployeeProfileModel, pk=pk)
    employee_username = employee.userprofile.user.username
    user = get_object_or_404(User, username=employee_username)
    employee.delete()
    user.delete()
    return redirect('employee-all-employees')


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def get_employee_detail(request, pk):
    employee = employee_models.EmployeeProfileModel.objects.get(pk=pk)
    table_html = backend_utils._get_details_table(employee)
    return JsonResponse(
        table_html, safe=False
    )


"""here are all the views related to  vehicles 
   all the work related to vehicles while remaining
   in the employee section will be managed by this"""


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def all_vehicle(request):
    request_user = request.user
    request_user_name = request_user.username
    company = employee_models.EmployeeProfileModel.objects.get(userprofile__user__username=request_user_name)
    vehicles = vehicle_models.Vehicle.objects.filter(company=company.company)
    sort = request.GET.get('sort', None)
    if sort:
        vehicles = vehicles.order_by(sort)
    table = vehicle_tables.VehicleTableForEmployee(vehicles)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Vehicle",
                "href": reverse("employee-add-vehicle-manager"),
                "icon": "fa fa-plus"
            },
        ],
        'vehicle_count': len(vehicles),
        "page_title": "Vehicles",
        "subtitle": "All vehicles are listed here",
        "table": table,
        "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html")

    }
    return render(request, "dashboard/list-entries.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def add_vehicle(request):
    if request.method == "POST":
        request_user = request.user
        request_user_name = request_user.username
        company = employee_models.EmployeeProfileModel.objects.get(
            userprofile__user__username=request_user_name)
        company_id = company.company
        form = vehicle_forms.VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.company = company_id
            vehicle.save()
            return redirect("employee-all-vehicle-manager")
    else:
        form = vehicle_forms.VehicleForm()
        context = {
            "page_title": "Add Vehicles",
            "subtitle": "Here you can add the vehicles",
            "form1": form,
            "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html")
        }
    return render(request, "dashboard/add_or_edit.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(vehicle_models.Vehicle, pk=pk)
    if request.method == "POST":
        form = vehicle_forms.VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save()
            return redirect('employee-all-vehicle-manager')
    else:
        form = vehicle_forms.VehicleForm(instance=vehicle)
        context = {
            "form1": form,
            "page_title": "Edit Vehicles",
            "subtitle": "Here you can add the vehicles",
            "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html")
        }
    return render(request, "dashboard/add_or_edit.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def delete_vehicle(request, pk):
    delete = backend_utils._delete_table_entry(vehicle_models.Vehicle, pk)
    return redirect('employee-all-vehicle-manager')


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def get_vehicle_detail(request, pk):
    vehicle = vehicle_models.Vehicle.objects.get(pk=pk)
    table_html = backend_utils._get_details_table(vehicle)
    return JsonResponse(
        table_html, safe=False
    )


"""here are all the views related to  clients 
   all the work related to clients while remaining
   in the employee section will be managed by this"""


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def all_clients(request):
    request_user = request.user
    request_user_name = request_user.username
    company = employee_models.EmployeeProfileModel.objects.get(userprofile__user__username=request_user_name)
    clients = client_models.PersonalClientProfileModel.objects.filter(company=company.company)
    individual_clients = []
    corporate_clients = []
    for client in clients:
        if client.is_corporate_client == True:
            corporate_clients.append(client)
        else:
            individual_clients.append(client)
    sort = request.GET.get('sort', None)
    if sort:
        clients = clients.order_by(sort)
    table = client_tables.PersonalClientProfileTableForEmployee(clients)
    table_individual = client_tables.PersonalClientProfileTableForEmployee(individual_clients)

    table_corporate = client_tables.PersonalClientProfileTableForEmployee(corporate_clients)

    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Client",
                "href": reverse("employee-add-client-general-info"),
                "icon": "fa fa-plus"
            },
        ],
        'count': len(clients),
        "page_title": "Clients",
        "subtitle": "Here you can see the Clients  ",
        'table': table,
        'table_individual': table_individual,
        'table_corporate': table_corporate,
        "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html"),
        "client_form": 'its an add client form'
    }
    return render(request, "dashboard/list-entries.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def add_client_general_info(request):
    if request.method == "POST":

        username = request.user.username
        company = employee_models.EmployeeProfileModel.objects.get(
            userprofile__user__username=username)
        company_id = company.company
        form = client_forms.PersonalClientProfileForm(request.POST)
        userform = client_forms.UserForm(request.POST)
        if form.is_valid() and userform.is_valid():
            user = userform.save(commit=False)
            user.set_password(request.POST.get('password'))
            user = userform.save()
            role = "CLIENT"
            phone_no = request.POST.get('primary_phone')
            user_profile = account_models.UserProfile.objects.create(user=user, verification_code=random_digits(),
                                                                     email_verified=True,
                                                                     role=role, phone=phone_no)
            user_profile.save()
            client = form.save(commit=False)
            client.userprofile = user_profile
            client.company = company_id
            client.save()
            return redirect("employee-add-client-address-info", username=user.username)
    else:
        form = client_forms.PersonalClientProfileForm()
        userform = client_forms.UserForm()
    context = {
        "page_title": "Client's Information",
        "subtitle": "Here you can add client's details.",
        "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html"),
        "form1": userform,
        "form5": form,
    }
    return render(request, "dashboard/add_or_edit.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def add_client_address_info(request, username):
    if request.method == "POST":
        addressform = client_forms.AddressForm(request.POST)
        if addressform.is_valid():
            address = addressform.save()
            user_profile = get_object_or_404(account_models.UserProfile, user__username=username)
            user_profile.address = address
            user_profile.save()
            client = get_object_or_404(client_models.PersonalClientProfileModel,
                                           userprofile__user__username=username)
            if client.is_corporate_client == True:
                return redirect("employee-add-client-business-info", username=username)
            else:
                return redirect("employee-add-client-payment-info", username=username)
    else:
        addressform = client_forms.AddressForm()
    context = {
        "page_title": "Client Address Detail",
        "subtitle": "Here you can add the Address Information.",
        "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html"),
        "form4": addressform,
        # "form4_name": 'Address Detail',
    }
    return render(request, "dashboard/add_or_edit.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def add_client_business_info(request, username):
    if request.method == "POST":
        businessclientprofileform = client_forms.BusinessClientProfileForm(request.POST)
        if businessclientprofileform.is_valid():
            business = businessclientprofileform.save()
            client = get_object_or_404(client_models.PersonalClientProfileModel,
                                           userprofile__user__username=username)
            client.business_client = business
            client.save()
            return redirect("employee-add-client-payment-info", username=username)
    else:
        businessclientprofileform = client_forms.BusinessClientProfileForm()
    context = {
        "page_title": "Client Business Information",
        "subtitle": "Here you can add Business Information of client. ",
        "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html"),
        "form3": businessclientprofileform,
        # "form3_name": 'Business Information',

    }
    return render(request, "dashboard/add_or_edit.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def add_client_payment_info(request, username):
    if request.method == "POST":
        clientpaymentinfoform = client_forms.ClientPaymentInfoForm(request.POST)
        if clientpaymentinfoform.is_valid():
            payment = clientpaymentinfoform.save()
            client = get_object_or_404(client_models.PersonalClientProfileModel,
                                           userprofile__user__username=username)
            client.client_payment_info = payment
            client.save()
            return redirect("employee-all-clients")
    else:
        clientpaymentinfoform = client_forms.ClientPaymentInfoForm()
    context = {
        "skip_btn": [
            {
                "color_class": "btn-secondary btn-outline-default",
                "title": "Skip",
                "href": reverse("employee-all-clients"),
                "icon": "fa fa-step-forward"
            },
        ],
        "page_title": "Client Payment Details",
        "subtitle": "Here you can add client's payment information.",
        "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html"),
        "form2": clientpaymentinfoform,
        # "form2_name": 'Payment Details',

    }
    return render(request, "dashboard/add_or_edit.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def edit_clients(request, pk):
    client = get_object_or_404(client_models.PersonalClientProfileModel, pk=pk)
    if request.method == "POST":
        form = client_forms.EditPersonalClientProfileForm(request.POST, instance=client)
        clientpaymentinfoform = client_forms.EditClientPaymentInfoForm(request.POST,
                                                                       instance=client.client_payment_info)
        businessclientprofileform = client_forms.EditBusinessClientProfileForm(request.POST,
                                                                               instance=client.business_client)
        addressform = client_forms.AddressForm(request.POST, instance=client.userprofile.address)
        userform = client_forms.UserForm(request.POST, instance=client.userprofile.user)
        if form.is_valid() and clientpaymentinfoform.is_valid() and \
                businessclientprofileform.is_valid() and addressform.is_valid():
            client_details = client
            if clientpaymentinfoform.has_changed() == True and clientpaymentinfoform.data['card_number'] != '' and \
                    clientpaymentinfoform.data['card_name'] != '' and clientpaymentinfoform.data[
                'card_expiration_date'] != '' and clientpaymentinfoform.data['cvv'] != '':
                payment = clientpaymentinfoform.save()
                client_details.client_payment_info = payment
            if clientpaymentinfoform.has_changed() == True and clientpaymentinfoform.data['card_number'] == '' and \
                    clientpaymentinfoform.data['card_name'] == '' and clientpaymentinfoform.data[
                'card_expiration_date'] == '' and clientpaymentinfoform.data['cvv'] == '':
                client_details.client_payment_info.delete()
                client_details.client_payment_info = None

            if businessclientprofileform.has_changed() == True and businessclientprofileform.data[
                'business_name'] != '' and businessclientprofileform.data[
                'business_phone'] != '' and client.is_corporate_client == True:
                business = businessclientprofileform.save()
                client_details.business_client = business
            if businessclientprofileform.has_changed() == True and businessclientprofileform.data[
                'business_name'] == '' and businessclientprofileform.data[
                'business_phone'] == '' and client.is_corporate_client == False:
                client_details.business_client.delete()
                client_details.business_client = None
            address = addressform.save()
            user_details = userform.save()
            if client.is_corporate_client == True and businessclientprofileform.data[
                'business_name'] != '' and businessclientprofileform.data[
                'business_phone'] != '' and businessclientprofileform.data[
                'business_email'] != '':
                client_details.save()
            if client.is_corporate_client == False and businessclientprofileform.data[
                'business_name'] == '' and businessclientprofileform.data[
                'business_phone'] == '' and businessclientprofileform.data[
                'business_email'] == '':
                client_details.save()
            return redirect("employee-all-clients")
    else:
        form = client_forms.EditPersonalClientProfileForm(instance=client)
        clientpaymentinfoform = client_forms.EditClientPaymentInfoForm(instance=client.client_payment_info)
        businessclientprofileform = client_forms.EditBusinessClientProfileForm(instance=client.business_client)
        addressform = client_forms.AddressForm(instance=client.userprofile.address)
        userform = client_forms.UserForm(instance=client.userprofile.user)
    context = {
        "page_title": "Add Clients",
        "subtitle": "Here you can add the clients",
        "nav_bar": render_to_string("dashboard/company/manager/partials/nav.html"),
        "form1": userform,
        "form2": form,
        "form3": addressform,
        "form4": businessclientprofileform,
        "form5": clientpaymentinfoform,
    }
    return render(request, "dashboard/add_or_edit.html", context)


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def delete_clients(request, pk):
    client = get_object_or_404(client_models.PersonalClientProfileModel, pk=pk)
    client_username = client.userprofile.user.username
    client_business_data = client.business_client.id
    client_payment_data = client.client_payment_info.id
    user = get_object_or_404(User, username=client_username)
    client_payment_info = get_object_or_404(client_models.ClientPaymentInfoModel, id=client_payment_data)
    client_business_info = get_object_or_404(client_models.BusinessClientProfileModel, id=client_business_data)
    client_business_info.delete()
    client_payment_info.delete()
    user.delete()
    return redirect('employee-all-clients')


@user_passes_test(backend_decorators._is_manager_or_dispatcher)
def get_client_detail(request, pk):
    client = client_models.PersonalClientProfileModel.objects.get(pk=pk)
    table_html = backend_utils._get_details_table(client)
    return JsonResponse(table_html, safe=False)
