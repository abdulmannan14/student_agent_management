from datetime import datetime, timedelta, date

from dateutil.relativedelta import relativedelta

import stripe

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from Account import utils as account_utils
from limoucloud_backend import utils as backend_utils
from Reservation import models as reservation_models
from Employee import models as employee_models
from Vehicle import models as vehicle_models
from Client import models as client_models
from . import models as company_models, urls as company_urls


def get_sum_of_all_reservation_fares(reservations):
    sum_final = []
    for i in reservations:
        amount = i.total_fare
        amount = int(amount)
        sum_final.append(amount)

    sum_final = sum(sum_final)
    return sum_final


def get_increment_percentage(clients=None, vehicles=None, reservation=None, employees=None, corporate_clients=None,
                             individual_clients=None):
    today = date.today()
    if clients:
        last_month_data = clients.filter(created_at__gte=(today - timedelta(days=30)))
        get_percentage = (len(last_month_data) / len(clients)) * 100
        get_percentage = round(get_percentage, 1)
    elif corporate_clients:
        last_month_corporate_client = corporate_clients.filter(created_at__gte=(today - timedelta(days=30)))
        get_percentage = (len(last_month_corporate_client) / len(corporate_clients)) * 100
        get_percentage = round(get_percentage, 1)
    elif individual_clients:
        last_month_individual_client = individual_clients.filter(created_at__gte=(today - timedelta(days=30)))
        get_percentage = (len(last_month_individual_client) / len(individual_clients)) * 100
        get_percentage = round(get_percentage, 1)

    elif vehicles:
        last_month_data = vehicles.filter(created_at__gte=(today - timedelta(days=30)))
        get_percentage = (len(last_month_data) / len(clients)) * 100
        get_percentage = round(get_percentage, 1)
    elif reservation:
        last_month_data = reservation.filter(created_at__gte=(today - timedelta(days=30)))
        get_percentage = (len(last_month_data) / len(clients)) * 100
        get_percentage = round(get_percentage, 1)
    elif employees:
        last_month_data = employees.filter(created_at__gte=(today - timedelta(days=30)))
        get_percentage = (len(last_month_data) / len(clients)) * 100
        get_percentage = round(get_percentage, 1)
    else:
        get_percentage = 0
    return get_percentage


def send_emails_to_clients(client_lc_account=None, new_lc_account_of_client=None, client=None):
    if client_lc_account != new_lc_account_of_client and new_lc_account_of_client == "TRUE":

        context = {
            'message': f'Thank you   {client.userprofile.user.get_full_name()} ! your Client account has been activated now at LimouCloud!'
                       f'You can Log in into Limoucloud mobile app for client. '
                       f'You can contact Limoucloud Support for further information. '
                       f'Thankyou! '
                       f'Limoucloud Team. '}

        account_utils._thread_making(backend_utils.send_email,
                                     ["Welcome to LimouCloud", context, client.userprofile.user])
    elif client_lc_account != new_lc_account_of_client and new_lc_account_of_client == "FALSE":
        context = {
            'message': f'Thank you   {client.userprofile.user.get_full_name()} ! your Client account has been deactivated at LimouCloud!'
                       f'You cannot Log in into Limoucloud mobile app for client for now. '
                       f'You can contact Limoucloud Support for further information. '
                       f'Thankyou! '
                       f'Limoucloud Team. '}

        account_utils._thread_making(backend_utils.send_email,
                                     ["Welcome to LimouCloud", context, client.userprofile.user])


def get_driver_trips_info(request):
    get_request_user = request.user
    get_request_user_name = get_request_user.username
    reservation = reservation_models.Reservation.objects.filter(
        company__userprofile__user__username=get_request_user_name)
    today = date.today()
    completed_reservations = reservation.filter(reservation_status='COMPLETED')
    total_reservations = completed_reservations.count()
    drivers = employee_models.EmployeeProfileModel.objects.filter(employee_role='Driver')
    driver_trips_info = []
    for driver in drivers:
        driver_trip_weekly = completed_reservations.filter(driver=driver,
                                                           pick_up_date__gte=(today - timedelta(days=7))).values_list(
            'driver').count()
        driver_trip_monthly = completed_reservations.filter(driver=driver,
                                                            pick_up_date__gte=(today - timedelta(days=30))).values_list(
            'driver').count()
        driver_trip_yearly = completed_reservations.filter(driver=driver,
                                                           pick_up_date__gte=(today - timedelta(days=365))).values_list(
            'driver').count()
        total_trips_this_year = completed_reservations.filter(pick_up_date__gte=(today - timedelta(days=365))).count()
        try:
            driver_trip_yearly = driver_trip_yearly / total_trips_this_year * 100
        except:
            driver_trip_yearly = 0.0

        driver_trip_yearly = round(driver_trip_yearly, 2)
        driver_data = {
            "driver_name": driver.full_name,
            'driver_trip_weekly': driver_trip_weekly,
            'driver_trip_monthly': driver_trip_monthly,
            'driver_trip_yearly': driver_trip_yearly,

        }
        driver_trips_info.append(driver_data)

    return driver_trips_info


def get_vehicle_trips_info(request):
    get_request_user = request.user
    get_request_user_name = get_request_user.username
    reservation = reservation_models.Reservation.objects.filter(
        company__userprofile__user__username=get_request_user_name)
    today = date.today()
    vehicles = vehicle_models.Vehicle.objects.filter(
        company__userprofile__user__username=get_request_user_name)
    completed_reservations = reservation.filter(reservation_status='COMPLETED',
                                                pick_up_date__gte=(today - timedelta(days=7)))
    total_reservations = completed_reservations.count()
    vehicles_trips_info = []
    total_trip_fare = 0
    test_list = []
    temperor = []
    for vehicle in vehicles:
        vehicle_trip_information = completed_reservations.filter(vehicle=vehicle)
        count_of_reservations = vehicle_trip_information.count()
        try:
            vehicle_trips_per_week_percentage = (count_of_reservations / total_reservations) * 100
        except:
            vehicle_trips_per_week_percentage = 0.0
        for i in vehicle_trip_information:
            temperor.append(i.total_fare)
        vehicle_data = {
            "vehicle_name": vehicle.all_vehicle_name.name,
            'vehicle_trips_quantity': count_of_reservations,
            'vehicle_total_fare_amount': sum(temperor),
            'vehicle_trips_per_week_percentage': vehicle_trips_per_week_percentage,

        }
        test_list.append(vehicle_data)
        temperor.clear()
    return test_list


def saving_user_details(get_or_edit_user, get_or_edit_user_address, get_or_edit_user_profile):
    user = get_or_edit_user.save()
    address = get_or_edit_user_address.save()
    user_details = get_or_edit_user_profile.save(commit=False)
    user_details.user = user
    user_details.address = address
    user_details.save()


def get_trips_revenue(all_reservations):
    label_list = []
    data_list = []
    for reservation in all_reservations:
        break_pickup_date = str(reservation.pick_up_date)
        break_pickup_date = break_pickup_date.split('-')
        year = break_pickup_date[0]
        if year in label_list:
            current_fare = data_list[-1]
            new_sumup_fare = current_fare + reservation.total_fare
            update_data_list = data_list.remove(current_fare)
            data_list.append(new_sumup_fare)
        else:
            try:
                label_list.append(int(year))
                data_list.append(reservation.total_fare)
            except:
                label_list.append(0)
                data_list.append(reservation.total_fare)


def get_requested_graph_value(all_reservations, value):
    label_list = []
    data_list = []
    if value == 'year':
        for reservation in all_reservations:
            break_pickup_date = str(reservation.pick_up_date)
            break_pickup_date = break_pickup_date.split('-')
            year = break_pickup_date[0]
            if year in label_list:
                current_fare = data_list[-1]
                new_sumup_fare = current_fare + reservation.total_fare
                update_data_list = data_list.remove(current_fare)
                data_list.append(new_sumup_fare)
            else:
                label_list.append(int(year))
                data_list.append(reservation.total_fare)
    elif value == 'month':
        pass
    elif value == 'week':
        pass
    else:
        return False
    today = datetime.today()
    year = today.year
    month_list = ['jan', 'feb', 'march', 'may', 'june', 'july', 'aug', 'sep', 'oct', 'nov', 'dec']
    year_reservations = all_reservations.filter(pick_up_date__icontains=year)
    year_data = []
    counter = 0
    for reservation in year_reservations:
        month_year = '{month}-{year}'.format(month=month_list[counter], year=year)
        year_reservations = all_reservations.filter(pick_up_date__icontains=year)
        convert_in_k = reservation.total_fare / 1000
        year_data.append(convert_in_k)
        counter += 1


def add_to_datetime(start_date, days=0, months=0, years=0):
    return start_date + relativedelta(days=days, months=months, years=years)


def get_context(businessclientprofileform):
    context2 = {
        "title": "Business Method",
        "forms": [
            {
                'form_name': businessclientprofileform,
                'form_class': 'col-md-4'
            },
        ],
        "form_class": 'col-md-6',
        "icon": "fa fa-credit-card",

        "actions": [

            {
                "title": "Previous",
                "classes": "previous action-button-previous btn btn-info",
                "type": "button"
            },
            {
                "title": "Next",
                "classes": "next btn btn-primary action-button",
                "type": "button"
            }
        ]
    }
    return context2


def get_edit_client_context(user_form, clients_form, address_form, clientpaymentinfoform):
    context = {
        "page_title": "Add Client",
        "back_url": company_urls.all_clients(),
        "action": "",  # leave empty for same view
        'nav_conf': {
            'active_classes': ['clients'],
        },
        "cancel_button": {
            "title": "Cancel",
            "classes": "btn btn-outline-danger text-black",
            "type": "button",
            "href": reverse('company-all-clients')},
        "form_steps": [
            {
                "title": "Client Details",
                "form_class": 'col-md-4',
                "icon": "fa fa-user",
                "forms": [
                    {
                        'form_name': user_form,
                        'form_class': 'col-md-3'
                    },
                    {
                        'form_name': clients_form,
                        'form_class': 'col-md-6'
                    },
                    {
                        'form_name': address_form,
                        'form_class': 'col-md-6',
                        'client_form': 'client_form',
                    },
                ],
                "active": True,

                "actions": [
                    {
                        "title": "Next",
                        "classes": "next btn btn-primary",
                        "type": "button"
                    },
                ]
            },
            {
                "title": "Payment Method",

                "forms": [
                    {
                        'form_name': clientpaymentinfoform,
                        'form_class': 'col-md-4',
                        'card_fields': True,
                        # 'card_details': True,
                        # 'card_expiry': card_details[0],
                        # 'card_number': card_details[2],
                    },
                ],
                "form_class": 'col-md-6',
                "icon": "fa fa-credit-card",

                "actions": [

                    {
                        "title": "Previous",
                        "classes": "previous action-button-previous btn btn-info",
                        "type": "button"
                    },
                    {
                        "title": "Submit",
                        "classes": "next btn btn-primary action-button",
                        "type": "submit",
                        'href': reverse('company-all-clients'),
                    }
                ]
            }

        ],
    }
    return context


def get_client_overview_context(client, user_form, clients_form, address_form, clientpaymentinfoform):
    context = {
        "page_title": "Client Overview",
        "back_url": company_urls.all_clients(),
        "action": "",  # leave empty for same view
        'readonly': 'readonly',
        'nav_conf': {
            'active_classes': ['clients'],
        },
        "cancel_button": {
            "title": "Cancel",
            "classes": "btn btn-primary text-black",
            "type": "button",
            "href": reverse('company-all-clients')},

        "edit_client": {
            "title": "Edit Client",
            "classes": "btn btn-primary text-black",
            "type": "button",
            "href": reverse('company-edit-client', kwargs={'pk': client.id})},
        "delete_client": {
            "title": "Delete Client",
            "classes": "btn btn-outline-danger text-black",
            "type": "button",
            "href": reverse('company-delete-client', kwargs={'pk': client.id})},
        "form_steps": [
            {
                "title": "Client Details",
                "form_class": 'col-md-4',
                "icon": "fa fa-user",
                "forms": [
                    {
                        'form_name': user_form,
                        'form_class': 'col-md-3'
                    },
                    {
                        'form_name': clients_form,
                        'form_class': 'col-md-6'
                    },
                    {
                        'form_name': address_form,
                        'form_class': 'col-md-6',
                        'client_form': 'client_form',
                    },
                ],
                "active": True,

                "actions": [
                    {
                        "title": "Next",
                        "classes": "next btn btn-primary",
                        "type": "button"
                    },
                ]
            },
            {
                "title": "Payment Method",
                "forms": [
                    {
                        'form_name': clientpaymentinfoform,
                        'form_class': 'col-md-4'
                    },
                ],
                "form_class": 'col-md-6',
                "icon": "fa fa-credit-card",

                "actions": [

                    {
                        "title": "Previous",
                        "classes": "previous action-button-previous btn btn-primary",
                        "type": "button"
                    },
                    # {
                    #     "title": "Submit",
                    #     "classes": "next btn btn-primary action-button",
                    #     "type": "button",
                    # }
                ]
            }

        ],
    }
    return context


def get_add_client_context(user_form, clients_form, address_form, clientpaymentinfoform):
    context = {
        "page_title": "Add Client",
        "back_url": company_urls.all_clients(),
        "action": "",  # leave empty for same view
        'nav_conf': {
            'active_classes': ['clients'],
        },
        "cancel_button": {
            "title": "Cancel",
            "classes": "btn btn-outline-danger text-black",
            "type": "button",
            "href": reverse('company-all-clients'),
            'id': 'id_cancel'
        },

        "form_steps": [
            {
                "title": "Client Details",
                "form_class": 'col-md-4',
                "icon": "fa fa-user",
                "forms": [
                    {
                        'form_name': user_form,
                        'form_class': 'col-md-3'
                    },
                    {
                        'form_name': clients_form,
                        'form_class': 'col-md-6'
                    },
                    {
                        'form_name': address_form,
                        'form_class': 'col-md-6',
                        'client_form': 'client_form',
                    },
                ],
                "active": True,

                "actions": [
                    {
                        "title": "Next",
                        "classes": "next btn btn-primary",
                        "type": "button"
                    },
                ]
            },
            {
                "title": "Payment Method",
                "forms": [
                    {
                        'form_name': clientpaymentinfoform,
                        'form_class': 'col-md-4',
                        'card_fields': True,
                    },
                ],
                "form_class": 'col-md-6',
                "icon": "fa fa-credit-card",

                "actions": [

                    {
                        "title": "Previous",
                        "classes": "previous action-button-previous btn btn-info",
                        "type": "button",
                        "id": "id_previous",
                    },
                    {
                        "title": "Next",
                        "classes": "next btn btn-primary action-button preview finish",
                        "type": "button",
                        # 'id': 'id_submit',
                        # 'href': reverse('company-all-clients'),
                    }
                ]
            },
            {
                "title": "Preview",
                'preview': 'preview',
                "forms": [

                ],
                "form_class": 'col-md-6',
                "icon": "fa fa-credit-card",

                "actions": [

                    # {
                    #     "title": "Previous",
                    #     "classes": "previous action-button-previous btn btn-info",
                    #     "type": "button",
                    #     "id": "id_previous",
                    # },
                    {
                        "title": "Submit",
                        "classes": "btn btn-primary action-button btn-submit",
                        "type": "submit",
                        # 'id': 'id_submit',
                        # 'href': reverse('company-all-clients'),
                    }
                ]
            }

        ],
    }
    return context


def add_client_card_details_to_stripe(client, request):
    cl = client.has_stripe_account()
    if cl is False:
        client_account = client.create_stripe_merchant_account()
    try:
        payment_method = stripe.PaymentMethod.create(type="card",
                                                     billing_details={
                                                         'name': request.POST.get('card_name'),
                                                     },
                                                     card={
                                                         "number": request.POST.get('card_number'),
                                                         "exp_month": request.POST.get('exp_month'),
                                                         "exp_year": request.POST.get('exp_year'),
                                                         "cvc": request.POST.get('cvv'),
                                                     },
                                                     )
        if payment_method:
            payment_method_id = payment_method['id']
            if payment_method_id:
                stripe.PaymentMethod.attach(payment_method_id, customer=client.merchant_account.stripe_id)
                return True
    except Exception as e:
        # messages.error(request, str(e))
        return False

    # account_utils._thread_making(attach_payment_method, arguments=[client])


def get_client_data(request):
    client_id = request.GET.get('client_id')
    client = client_models.PersonalClientProfileModel.objects.get(id=client_id)
    context = {
        'first_name': client.userprofile.user.first_name,
        'last_name': client.userprofile.user.last_name,
        'email': client.userprofile.user.email,
        'address': client.userprofile.address.address,
        'primary_phone': client.primary_phone,
        'secondary_phone': client.secondary_phone,
    }
    return JsonResponse(context, safe=False)


def get_company_from_user(user):
    """
    get company object from authenticated user
    param: user
    """
    try:
        return user.userprofile.employeeprofilemodel.company
    except:
        return user.userprofile.companyprofilemodel

    # finally:
    #     return user.userprofile.personalclientprofilemodel.company


def _get_client_card_details(company, client):
    print("this is client and company========", client, '======', company)
    company: company_models.CompanyProfileModel
    stripe.api_key = company.stripepayment_set.last().secret_key
    print("this is client and api key========", stripe.api_key)
    # stripe.api_key = settings.STRIPE_SECRET_KEY
    cards = stripe.PaymentMethod.list(customer=client.merchant_account.stripe_id, type="card").get("data", [])
    card_len = len(cards) - 1
    month = cards[0]['card']["exp_month"]
    datetime_object = datetime.strptime(str(month), "%m")
    month_name = datetime_object.strftime("%b")
    year = cards[0]['card']["exp_year"]
    type = cards[0]['card']["brand"]
    card_number = cards[0]['card']["last4"]
    return f"{month_name}-{year}", type, card_number
