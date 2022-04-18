from django.urls import reverse

import Client.models
import Client.models as client_models
import Reservation.calculate_fare
from setting import models as setting_models
from Reservation import models as reservation_models, forms as reservation_forms, \
    calculate_fare as reservation_calculate_fare
from Account.utils import _thread_making
from limoucloud_backend import decorators as backend_decorators, utils as backend_utils
from Company import urls as company_urls
from math import sin, cos, sqrt, atan2, radians
from setting import utils as setting_utils
from Home import models as home_models
from Employee import models as employee_models
from Merchants.stripe import utils as merchant_stripe_utils
from limoucloud_backend.utils import success_response_fe, failure_response_fe


def get_reservations(all_reservations, company, charge_by=None, status_type=None, vehicle_type=None,
                     pay_by=None):
    if charge_by and charge_by != 'ALL':
        all_reservations = all_reservations.filter(company=company,
                                                   charge_by=charge_by)
    if status_type and status_type != 'ALL':
        all_reservations = all_reservations.filter(company=company,
                                                   reservation_status=status_type)
    if pay_by and pay_by != 'ALL':
        all_reservations = all_reservations.filter(company=company, pay_by=pay_by)
    if vehicle_type and vehicle_type != 'ALL':
        all_reservations = all_reservations.filter(company=company,
                                                   vehicle_type=vehicle_type)

    return all_reservations


def stops_choices(stops=9):
    choices = []
    for i in range(0, stops):
        option = "{}".format(i)
        choices.append((option, option))
    return choices


def get_taxes(tolls, meet_and_greet, gratuity_percentage,
              fuel_Surcharge_percentage, sales_tax_percentage,
              discount_percentage, additional_passenger_charge, additional_luggage_charge, additional_stops_charge):
    taxes = [
        {
            'name': 'tolls',
            'id': 'id_tolls',
            'value': tolls
        },
        {
            'name': 'meet_and_greet',
            'id': 'id_meet_and_greet',
            'value': meet_and_greet
        },
        {
            'name': 'gratuity_percentage',
            'id': 'id_gratuity_percentage',
            'value': gratuity_percentage
        },
        {
            'name': 'fuel_Surcharge_percentage',
            'id': 'id_fuel_Surcharge_percentage',
            'value': fuel_Surcharge_percentage
        },
        {
            'name': 'sales_tax_percentage',
            'id': 'id_sales_tax_percentage',
            'value': sales_tax_percentage
        },
        {
            'name': 'discount_percentage',
            'id': 'id_discount_percentage',
            'value': discount_percentage
        },
        {
            'name': 'additional_passenger_charge',
            'id': 'id_additional_passenger_charge',
            'value': additional_passenger_charge
        },
        {
            'name': 'additional_luggage_charge',
            'id': 'id_additional_luggage_charge',
            'value': additional_luggage_charge
        },
        {
            'name': 'additional_stops_charge',
            'id': 'id_additional_stops_charge',
            'value': additional_stops_charge
        },
    ]
    return taxes


def get_service_price_details(selected_vehicle_type, passenger_quantity, luggage_bags_quantity, selected_stops,
                              additional_passenger_price, additional_luggage_price, additional_stops_price):
    charges_of_extra_passengers = 0
    charges_of_extra_luggage = 0
    charges_of_extra_stops = 0
    total_additional_charges = 0
    get_vehicle_type_details = setting_models.VehicleType.objects.get(id=selected_vehicle_type)
    max_passenger = get_vehicle_type_details.max_passengers
    max_luggage = get_vehicle_type_details.max_luggage
    passenger_quantity = int(passenger_quantity)
    luggage_bags_quantity = int(luggage_bags_quantity)
    selected_stops = int(selected_stops)
    if passenger_quantity < max_passenger and luggage_bags_quantity < max_luggage and selected_stops == 0:
        return total_additional_charges
    if passenger_quantity > max_passenger:
        extra_passenger = passenger_quantity - max_passenger
        charges_of_extra_passengers = extra_passenger * additional_passenger_price
    if luggage_bags_quantity > max_luggage:
        extra_luggage = luggage_bags_quantity - max_luggage
        charges_of_extra_luggage = extra_luggage * additional_luggage_price
    if selected_stops > 0:
        charges_of_extra_stops = selected_stops * additional_stops_price

    total_additional_charges = charges_of_extra_passengers + charges_of_extra_luggage + charges_of_extra_stops
    return total_additional_charges


def parse_geo_address(request=None, name="pickup"):
    address = request.POST.get('{}_address'.format(name), "")
    coordinates = request.POST.get('{}_latlong'.format(name), "")
    lat_lng = coordinates.split(',')
    lat, lng = (lat_lng[0], lat_lng[1]) if lat_lng.__len__() > 1 else (0, 0)
    return reservation_models.GeoAddress(
        address=address,
        latitude=lat,
        longitude=lng
    )


def get_trip_cordinates(pickup_cordinates, destiantion_cordinates, pickup_address_name, destination_address_name):
    try:
        pickup_split = pickup_cordinates.split(',')
        pickup_lat = pickup_split[0]
        pickup_lng = pickup_split[1]
        adding_geo_for_pickup = reservation_models.GeoAddress.objects.create(longitude=pickup_lng, latitude=pickup_lat,
                                                                             address=pickup_address_name)
        destination_split = destiantion_cordinates.split(',')
        destination_lat = destination_split[0]
        destination_lng = destination_split[1]
        adding_geo_for_destination = reservation_models.GeoAddress.objects.create(longitude=destination_lng,
                                                                                  latitude=destination_lat,
                                                                                  address=destination_address_name)
        return adding_geo_for_pickup, adding_geo_for_destination
    except:
        return None


def get_service_price(request, selected_vehicle_type, selected_service_type, selected_charge_by):
    try:
        get_service_price = setting_models.ServicePrice.objects.get(vehicle_type=selected_vehicle_type,
                                                                    service_type=selected_service_type,
                                                                    price_type=selected_charge_by)
        additional_passenger_price = get_service_price.per_additional_passenger
        additional_luggage_price = get_service_price.per_additional_luggage
        additional_stops_price = get_service_price.per_additional_stop
    except:
        additional_passenger_price = request.POST.get('additional_passenger_price', 0)
        additional_luggage_price = request.POST.get('additional_luggage_price', 0)
        additional_stops_price = request.POST.get('additional_stops_price', 0)

    return additional_passenger_price, additional_luggage_price, additional_stops_price


def sending_email_to_driver(driver, pickup_date, pickup_time, pickup_address, destination_address, get_driver):
    context = {
        'subject': "New Reservation",
        'message': 'Hello <strong>{driver}</strong> ! We have got a new reservation for you! Following are the details:'
                   '<br>'
                   ' Date: <strong>{pickup_date}</strong> '
                   '<br>'
                   ' Time: <strong>{pickup_time}</strong> '
                   '<br>'
                   ' Pickup Location: <strong>{pickup_address}</strong> '
                   '<br>'
                   ' Dropoff Location: <strong>{destination_address}</strong> '
                   '<br>'
                   ' For further detail please see your mobile app. '.format(driver=driver, pickup_date=pickup_date,
                                                                             pickup_time=pickup_time,
                                                                             pickup_address=pickup_address,
                                                                             destination_address=destination_address)
    }
    _thread_making(backend_utils.send_email, ['LimouCloud New Reservation', context, get_driver])
    return True


def sending_email_to_client(client, pickup_date, pickup_time, pickup_address, destination_address, get_client,
                            reservation_status, edit=None):
    context = {
        'subject': f"Hello {client} your Reservation is Booked at LimouCloud",
        'message': ' Following are the details:'
                   '<br>'
                   ' Reservation Status: <strong>{status}</strong> '
                   '<br>'
                   ' Date: <strong>{pickup_date}</strong> '
                   '<br>'
                   ' Time: <strong>{pickup_time}</strong> '
                   '<br>'
                   ' Pickup Location: <strong>{pickup_address}</strong> '
                   '<br>'
                   ' Dropoff Location: <strong>{destination_address}</strong> '
                   '<br>'
                   ' For further detail please see your mobile app. '.format(status=reservation_status,
                                                                             pickup_date=pickup_date,
                                                                             pickup_time=pickup_time,
                                                                             pickup_address=pickup_address,
                                                                             destination_address=destination_address)
    }
    if edit:
        subject = f"Hello {client} your Reservation Status is updated"
        context['subject'] = subject
    _thread_making(backend_utils.send_email, ['LimouCloud New Reservation', context, get_client])
    return True


def cals_acc_to_charge_type(reservation, request):
    fare_amount = float(request.POST.get('base_fare', 0))
    duration = request.POST.get('duration', 0)
    charge_by = request.POST.get('charge_by', '')
    distance_in_miles = request.POST.get('distance_in_miles', 0)
    rate_per_mile = request.POST.get('rate_per_mile', 0)
    from_date = request.POST.get('from_date', '')
    to_date = request.POST.get('to_date', '')
    no_of_days = request.POST.get('no_of_days', 0)
    rate_per_day = request.POST.get('rate_per_day', 0)

    if charge_by == 'FLAT RATE':
        reservation.duration = duration
        reservation.base_fare = fare_amount
    elif charge_by == 'HOURLY RATE':
        hour_rate = backend_utils._get_hours_rate(request)
        rate_of_total_hours = (hour_rate[0])
        total_hours = (hour_rate[1])
        reservation.total_hours = total_hours
        fare_amount = rate_of_total_hours
        reservation.base_fare = fare_amount
    elif charge_by == 'DISTANCE RATE':
        reservation.distance_in_miles = distance_in_miles
        reservation.base_fare = fare_amount
        reservation.rate_per_mile = rate_per_mile
        # distance_fare = int(rate_per_mile) * float(distance_in_miles)
        # fare_amount = int(fare_amount) + int(distance_fare)

    elif charge_by == 'DAILY RATE':
        reservation.from_date = from_date
        reservation.to_date = to_date
        reservation.no_of_days = no_of_days
        reservation.rate_per_day = rate_per_day
        reservation.base_fare = fare_amount
    else:
        pass
    reservation.save()


def get_stops_for_view_edit_reservation(reservation):
    stops = reservation.stops_address.values()
    stops_details = []
    for stop in stops:
        stops_dict = {
            'name': stop['address'],
            'lat': str(stop['latitude']),
            'long': str(stop['longitude'])
        }
        stops_details.append(stops_dict)
    return stops_details


def get_reservation_overview_context(reservation_form_pickup_dropoff_info_only_service_type,
                                     client_form, reservation_form_vehicle_and_driver_info,
                                     reservation_form_client_and_driver_notes_info,
                                     reservation_form_charge_by_info,
                                     form1, FormForFirstLastNameEmail, reservation):
    reservation_stops = get_stops_for_view_edit_reservation(reservation)
    context = {
        'reservation': reservation_stops,
        'reservation_id': reservation.id,
        'reservation_obj': reservation,
        "page_title": "New Reservation",
        "back_url": company_urls.all_reservation(),
        "action": "",  # leave empty for same view
        'readonly': 'readonly',
        "cancel_button": {
            "title": "Cancel",
            "classes": "btn btn-outline-danger text-black",
            "type": "button",
            "href": reverse('company-all-reservations'),
            'id': 'id_cancel'
        },
        "edit_reservation": {
            "title": "Edit Reservation",
            "classes": "btn btn-primary text-black",
            "type": "button",
            "href": reverse('company-edit-reservations', kwargs={'pk': reservation.id})
        },

        "form_steps": [
            {
                "title": "Trip Details",
                "form_class": 'col-md-4',
                "icon": "fa fa-user",
                'firstpage': 'firstpage',
                "forms": [
                    {
                        'form_name': reservation_form_pickup_dropoff_info_only_service_type,
                        'form_class': 'col-md-4',
                        'class_name': 'calculate_fare',
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
                "title": "Client Details",
                'check': 'check',
                'FormForFirstLastNameEmail': FormForFirstLastNameEmail,
                "forms": [
                    {
                        'form_name': client_form,
                        'form_class': 'col-md-4',
                        'add_client': True,
                    },
                ],
                "form_class": 'col-md-6',
                "icon": "fa fa-address-card-o",
                "actions": [
                    {
                        "title": "Previous",
                        "classes": "previous action-button-previous btn btn-info",
                        "type": "button",
                        "id": "id_previous",
                    },
                    {
                        "title": "Next",
                        "classes": "next btn btn-primary action-button",
                        "type": "button",

                    }
                ]
            },
            {
                "title": "Vehicle & Driver Details",
                "forms": [
                    {
                        'form_name': reservation_form_vehicle_and_driver_info,
                        'form_class': 'col-md-4',

                    },
                    {
                        'form_name': reservation_form_client_and_driver_notes_info,
                        'form_class': 'col-md-4',

                    },
                ],
                "form_class": 'col-md-6',
                "icon": "fa fa-car",

                "actions": [

                    {
                        "title": "Previous",
                        "classes": "previous action-button-previous btn btn-info",
                        "type": "button",
                        "id": "id_previous",
                    },
                    {
                        "title": "Next",
                        "classes": "next btn btn-primary action-button",
                        "type": "button",

                    }
                ]
            },
            {
                "title": "Pricing",
                "forms": [
                    {
                        'form_name': reservation_form_charge_by_info,
                        'form_class': 'col-md-4',
                        'class_name': 'calculate_fare',

                    },
                    {
                        'form_name': form1,
                        'form_class': 'col-md-4',
                        'class_name': 'calculate_fare',

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

                ]
            },

        ],
        'nav_conf': {
            'active_classes': ['reservations'],
        },
    }
    return context


def get_add_reservation_context(reservation_form_pickup_dropoff_info_only_service_type,
                                client_form, reservation_form_vehicle_and_driver_info,
                                reservation_form_client_and_driver_notes_info,
                                reservation_form_charge_by_info,
                                form1, FormForFirstLastNameEmail, reservation=None):
    if reservation:
        reservation_stops = get_stops_for_view_edit_reservation(reservation)
        reservation_id = reservation.id
    else:
        reservation_stops = ''
        reservation_id = 0

    context = {
        'reservation': reservation_stops,
        'reservation_id': reservation_id,
        'reservation_obj': reservation,
        "page_title": "New Reservation",
        "back_url": company_urls.all_reservation(),
        "action": "",  # leave empty for same view
        "cancel_button": {
            "title": "Cancel",
            "classes": "btn btn-outline-danger text-black",
            "type": "button",
            "href": reverse('company-all-reservations'),
            'id': 'id_cancel'
        },
        # "edit_reservation": {
        #     "title": "Edit Reservation",
        #     "classes": "btn btn-primary text-black",
        #     "type": "button",
        #     "href": reverse('company-edit-reservations', kwargs={'pk': reservation.id})
        # },

        "form_steps": [
            {
                "title": "Trip Details",
                "form_class": 'col-md-4',
                "icon": "fa fa-user",
                'firstpage': 'firstpage',
                "forms": [

                    {
                        'form_name': reservation_form_pickup_dropoff_info_only_service_type,
                        'form_class': 'col-md-4',
                        'class_name': 'calculate_fare',
                    },

                ],
                "active": True,
                "actions": [
                    {
                        "title": "Next",
                        "classes": "next btn btn-primary finish",
                        "type": "button"
                    },
                ]
            },
            {
                "title": "Client Details",
                'check': 'check',
                'FormForFirstLastNameEmail': FormForFirstLastNameEmail,
                "forms": [
                    {
                        'form_name': client_form,
                        'form_class': 'col-md-4',
                        'add_client': True,
                    },
                ],
                "form_class": 'col-md-6',
                "icon": "fa fa-address-card-o",
                "actions": [
                    {
                        "title": "Previous",
                        "classes": "previous action-button-previous btn btn-info finish",
                        "type": "button",
                        "id": "id_previous",
                    },
                    {
                        "title": "Next",
                        "classes": "next btn btn-primary action-button finish",
                        "type": "button",
                        # 'id': 'id_submit',
                        # 'href': reverse('company-all-clients'),
                    }
                ]
            },
            {
                "title": "Vehicle & Driver Details",
                "forms": [
                    {
                        'form_name': reservation_form_vehicle_and_driver_info,
                        'form_class': 'col-md-4',

                    },
                    {
                        'form_name': reservation_form_client_and_driver_notes_info,
                        'form_class': 'col-md-4',

                    },
                ],
                "form_class": 'col-md-6',
                "icon": "fa fa-car",

                "actions": [

                    {
                        "title": "Previous",
                        "classes": "previous action-button-previous btn btn-info finish",
                        "type": "button",
                        "id": "id_previous",
                    },
                    {
                        "title": "Next",
                        "classes": "next btn btn-primary action-button finish",
                        "type": "button",
                        # 'id': 'id_submit',
                        # 'href': reverse('company-all-clients'),
                    }
                ]
            },
            {
                "title": "Pricing",
                "forms": [
                    {
                        'form_name': reservation_form_charge_by_info,
                        'form_class': 'col-md-4',
                        'class_name': 'calculate_fare',

                    },
                    {
                        'form_name': form1,
                        'form_class': 'col-md-4',
                        'class_name': 'calculate_fare',

                    },
                ],
                "form_class": 'col-md-6',
                "icon": "fa fa-credit-card",

                "actions": [

                    {
                        "title": "Previous",
                        "classes": "previous action-button-previous btn btn-info finish",
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
                "title": "Trip Preview",
                'preview': 'preview',
                "forms": [
                    # {
                    #     'form_name': reservation_form_pickup_dropoff_info_only_service_type,
                    #     'form_class': 'col-md-4',
                    #     'class_name': 'calculate_fare',
                    # },
                    # {
                    #     'form_name': client_form,
                    #     'form_class': 'col-md-4',
                    #     'add_client': True,
                    # },
                    # {
                    #     'form_name': reservation_form_vehicle_and_driver_info,
                    #     'form_class': 'col-md-4',
                    #
                    # },
                    # {
                    #     'form_name': reservation_form_client_and_driver_notes_info,
                    #     'form_class': 'col-md-4',
                    #
                    # },
                    # {
                    #     'form_name': reservation_form_charge_by_info,
                    #     'form_class': 'col-md-4',
                    #     'class_name': 'calculate_fare',
                    #
                    # },
                    # {
                    #     'form_name': form1,
                    #     'form_class': 'col-md-4',
                    #     'class_name': 'calculate_fare',
                    #
                    # },
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
        'nav_conf': {
            'active_classes': ['reservations'],
        },
    }
    return context


def additional_passenger_luggage_fare(request, vehicle_type):
    passenger_quantity = request.GET.get('passenger_quantity', 1)
    passenger_quantity = int(passenger_quantity)
    luggage_quantity = int(request.GET.get('luggage_quantity', 1))
    # luggage_quantity = int(luggage_quantity)
    additional_per_passenger_charge = request.GET.get('additional_per_passenger_charge', 0)
    additional_per_passenger_charge = int(additional_per_passenger_charge)
    additional_per_luggage_charge = request.GET.get('additional_per_luggage_charge', 0)
    stops = int(request.GET.get('stops', 0))
    additional_per_stops_charge = float(request.GET.get('additional_per_stops_charge', 0))
    additional_per_luggage_charge = int(additional_per_luggage_charge)
    vehicle_type_obj = setting_models.VehicleType.objects.get(id=vehicle_type)
    max_passengers = vehicle_type_obj.max_passengers
    max_luggage = vehicle_type_obj.max_luggage
    passenger_fare = 0
    luggage_fare = 0
    stops_fare = 0
    if max_passengers < passenger_quantity:
        passenger_fare = (passenger_quantity - max_passengers) * additional_per_passenger_charge
    if max_luggage < luggage_quantity:
        luggage_fare = (luggage_quantity - max_luggage) * additional_per_luggage_charge
    if stops > 0:
        stops_fare = stops * additional_per_stops_charge
    return passenger_fare, luggage_fare, stops_fare


# def get_stops_lat_long(stop_1=None, stop_2=None, stop_3=None, stop_4=None, stop_5=None, stop_6=None,
#                        stop_7=None, stop_8=None):
#     li = [stop_1, stop_2, stop_3, stop_4, stop_5, stop_6, stop_7, stop_8]
#     stops_cordinates = []
#     for i in range(8):
#         if li[i]:
#             stop = li[i]
#             stop_split = stop.split(',')
#             stop_lat = stop_split[0]
#             stop_lng = stop_split[1]
#             stops_cordinates.append(stop_lat)
#             stops_cordinates.append(stop_lng)
#         else:
#             stops_cordinates.append(0)
#             stops_cordinates.append(0)
#     return stops_cordinates


def get_lat_long(pickup_cordinates, destiantion_cordinates):
    try:
        pickup_split = pickup_cordinates.split(',')
        pickup_lat = pickup_split[0]
        pickup_lng = pickup_split[1]
        destination_split = destiantion_cordinates.split(',')
        destination_lat = destination_split[0]
        destination_lng = destination_split[1]

        return pickup_lat, pickup_lng, destination_lat, destination_lng
    except:
        return True


def calculate_reservation_fare_frontend(request):
    base_fare = float(request.GET.get('base_fare', 0))
    charge_by = request.GET.get('charge_by', 0)
    duration = request.GET.get('duration', 0)
    deposit_amount = float(request.GET.get('deposit_amount', ''))
    gratuity_percentage = float(request.GET.get('gratuity_percentage', 0))
    fuel_surcharge_percentage = float(request.GET.get('fuel_surcharge_percentage', 0))
    discount_percentage = float(request.GET.get('discount_percentage', 0))
    sales_tax_percentage = float(request.GET.get('sales_tax_percentage', 0))
    tolls = float(request.GET.get('tolls', 0))
    meet_and_greet = float(request.GET.get('meet_and_greet', 0))
    vehicle_type = request.GET.get('vehicle_type', 0)
    pickup_latlong = request.GET.get('pickup_latlong', 0)
    destination_latlong = request.GET.get('destination_latlong', 0)

    if charge_by == 'FLAT RATE':
        base_fare = base_fare
    elif charge_by == 'HOURLY RATE':
        try:
            hours_fare = int(request.GET.get('hours_fare', 0))
        except:
            hours_fare = 0
        base_fare = hours_fare
    elif charge_by == 'DISTANCE RATE':
        fare_amount = request.GET.get('fare_amount', 0)
        base_fare = base_fare
        base_fare = float(fare_amount) + base_fare
    elif charge_by == 'DAILY RATE':
        base_fare = base_fare

    # deposit_amount = int(deposit_amount)
    gratuity_percentage_value = (base_fare / 100) * gratuity_percentage
    fuel_Surcharge_percentage_value = (base_fare / 100) * fuel_surcharge_percentage
    discount_percentage_value = (base_fare / 100) * discount_percentage
    sales_tax_percentage_value = (base_fare / 100) * sales_tax_percentage
    pending_fare_amount = base_fare + gratuity_percentage_value + fuel_Surcharge_percentage_value + sales_tax_percentage_value + tolls + meet_and_greet
    pending_fare_amount = pending_fare_amount - discount_percentage_value
    # pending_fare_amount = pending_fare_amount - discount_percentage_value - deposit_amount
    pending_fare_amount = float(pending_fare_amount)
    pending_fare_amount = str(round(pending_fare_amount, 2))
    total_fare = float(pending_fare_amount)
    extra_passenger_luggage_fare = additional_passenger_luggage_fare(request, vehicle_type)

    # total_fare = float(pending_fare_amount) + int(deposit_amount)
    total_fare = round(total_fare, 2)
    total_fare = total_fare + extra_passenger_luggage_fare[0] + extra_passenger_luggage_fare[1] + \
                 extra_passenger_luggage_fare[2]
    balance_fare = total_fare - deposit_amount
    return total_fare, balance_fare


def add_other_reservation_details(reservation, request):
    deposit_type = request.POST.get('deposit_type')
    pickup_date = request.POST.get('pick_up_date')
    pickup_time = request.POST.get('pick_up_time')
    service_type = request.POST.get('service_type')
    duration = request.POST.get('duration', '')
    reservation_status = request.POST.get('reservation_status')
    passenger_quantity = request.POST.get('passenger_quantity')
    luggage_bags_quantity = request.POST.get('luggage_bags_quantity')
    stops_between_ride = request.POST.get('stops_between_ride')
    reservation.deposit_type = deposit_type
    reservation.pick_up_date = pickup_date
    reservation.pick_up_time = pickup_time
    reservation.duration = duration
    service_type = setting_utils.get_service_type(service_type)
    reservation.service_type = service_type
    reservation.reservation_status = reservation_status
    reservation.passenger_quantity = passenger_quantity
    reservation.luggage_bags_quantity = luggage_bags_quantity
    if stops_between_ride == reservation.stops_between_ride:
        pass
    else:
        reservation.stops_between_ride = stops_between_ride
    reservation.save()


def saving_reservation_details(request, reservation, company, adding_geo_for_pickup, adding_geo_for_destination):
    reservation.company = company
    reservation.pickup_address = adding_geo_for_pickup
    reservation.destination_address = adding_geo_for_destination
    form_client = reservation_forms.ReservationFormClientInfo(request.POST, instance=reservation)
    form_client.save()
    form_reservation_client_and_driver_notes_info = reservation_forms.ReservationFormClientAndDriverNotesInfo(
        request.POST, instance=reservation)
    form_reservation_client_and_driver_notes_info.save()
    form_reservation_charge_by_info = reservation_forms.ReservationFormChargeByInfo(request.POST,
                                                                                    instance=reservation)
    form_reservation_charge_by_info.save()
    form_form1 = reservation_forms.ReservationFormGratuityFuelSurchargeInfo(request.POST, instance=reservation)
    form_form1.save()


def adding_stops_to_geo_address(request, reservation):
    stops_quantity = int(request.POST.get('stops_between_ride'))
    for stop in range(stops_quantity):
        stop_name = request.POST.get('{stop} stop'.format(stop=stop + 1))
        stop_latlong = request.POST.get('stops_latlong_{stop}'.format(stop=stop + 1))
        lat_lng = stop_latlong.split(',')
        lat, lng = (lat_lng[0], lat_lng[1]) if lat_lng.__len__() > 1 else (0, 0)
        geo_addrress = reservation_models.GeoAddress.objects.create(longitude=lng, latitude=lat,
                                                                    address=stop_name)
        geo_addrress.save()
        reservation.stops_address.add(geo_addrress)
        reservation.save()


def check_stops_addresses_are_same_or_changed(request, reservation):
    stops_quantity = int(request.POST.get('stops_between_ride'))
    all_stops_addresses_in_reservation = reservation.stops_address.all()
    for stop in range(stops_quantity):
        stop_name = request.POST.get('{stop} stop'.format(stop=stop + 1))
        if str(all_stops_addresses_in_reservation[stop]) == stop_name:
            return False
        else:
            return True


def _get_total_distance_including_all_added_stops(addresses):
    distance = 0
    try:
        addresses = list(filter(lambda a: a != 0, addresses))
        for i in range(len(addresses) - 1):
            if addresses[i] != 0 and addresses[i + 1] != 0:
                seperating = get_lat_long(addresses[i], addresses[i + 1])
                dist = reservation_calculate_fare.calculate_distance(start_lat=seperating[0], start_lng=seperating[1],
                                                                     end_lat=seperating[2], end_lng=seperating[3])
                distance += dist
        return distance
    except:
        distance = 0


def get_reservation_record_message_type(status):
    message = 'New Reservation'
    if status == 'QUOTED':
        message = 'Quote Sent'
    elif status == 'CONFIRMED':
        message = 'Reservation Confirmed'
    elif status == 'SCHEDULED':
        message = 'Reservation Scheduled'
    elif status == 'COMPLETED':
        message = 'Reservation Completed'
    elif status == 'CANCELLED':
        message = 'Reservation Cancelled'
    elif status == 'REQUESTED':
        message = 'Reservation Requested'
    return message


def save_record(request, reservation, company):
    sender = request.user.userprofile.role
    complete_sender = "{user}({role})".format(user=request.user.get_full_name(), role=sender)
    message_type = get_reservation_record_message_type(request.POST.get('reservation_status'))
    save_record_driver = home_models.Email.objects.create(date=reservation.pick_up_date, client=reservation.client,
                                                          send_to=reservation.client.userprofile.user.email,
                                                          message_type=message_type, sender=complete_sender,
                                                          reservation=reservation.id, company=company)
    # save_record_client = home_models.Email.objects.create(date=reservation.pick_up_date, client=reservation.client,
    #                                                       send_to=reservation.client.userprofile.user.email,
    #                                                       message_type=message_type, sender=complete_sender,
    #                                                       reservation=reservation.id, company=company)
    return True


def sending_and_saving_email(reservation, request, company):
    driver = request.POST.get('driver')
    get_driver = employee_models.EmployeeProfileModel.objects.get(id=driver)
    get_driver_username = get_driver.userprofile.user.username
    sending_email = sending_email_to_driver(get_driver_username, reservation.pick_up_date, reservation.pick_up_time,
                                            reservation.pickup_address, reservation.destination_address, get_driver)
    sending_email = sending_email_to_client(reservation.client.userprofile.user.username, reservation.pick_up_date,
                                            reservation.pick_up_time, reservation.pickup_address,
                                            reservation.destination_address, reservation.client.userprofile.user,
                                            reservation.reservation_status)
    save_mail = save_record(request, reservation, company)


def sending_and_saving_email_for_client(reservation, request, company):
    sending_email = sending_email_to_client(reservation.client.userprofile.user.username, reservation.pick_up_date,
                                            reservation.pick_up_time, reservation.pickup_address,
                                            reservation.destination_address, reservation.client.userprofile.user,
                                            request.POST.get('reservation_status'), edit=True)
    save_mail = save_record(request, reservation, company)


def check_deposit_amount_and_transfer_funds(request, client):
    if float(request.POST.get('deposit_amount')) > 0:
        client: client_models.PersonalClientProfileModel
        if client.merchant_account and client.merchant_account.stripe_id:
            try:
                making_payment = merchant_stripe_utils.create_payment_intent(client.merchant_account.stripe_id,
                                                                             amount=int(float(request.POST.get(
                                                                                 'deposit_amount')) * 100),
                                                                             company=client.company)
                making_payment.confirm(making_payment['id'], payment_method='pm_card_visa', )
                return success_response_fe()
            except Exception as e:
                return failure_response_fe(msg="Something Went Wrong, Transaction does'nt complete")
        else:
            return failure_response_fe(msg="No Payment Method Attached")
    else:
        return success_response_fe()


def for_edit_check_deposit_amount_and_transfer_funds(request, client, reservation, deposit_amount):
    if float(request.POST.get('deposit_amount')) > deposit_amount:
        client: client_models.PersonalClientProfileModel
        if client.merchant_account and client.merchant_account.stripe_id:
            try:
                deposit = float(request.POST.get('deposit_amount')) - deposit_amount
                making_payment = merchant_stripe_utils.create_payment_intent(client.merchant_account.stripe_id,
                                                                             amount=int(float(deposit) * 100),
                                                                             company=client.company)
                making_payment.confirm(making_payment['id'], payment_method='pm_card_visa', )
                return success_response_fe()

            except Exception as e:
                return failure_response_fe(msg="Something Went Wrong, Transaction does'nt complete")
        else:
            return failure_response_fe(msg="No Payment Method Attached")
    elif float(request.POST.get('deposit_amount')) == deposit_amount:
        return success_response_fe()
    else:
        return failure_response_fe(msg=f'You cannot decrease your deposit amount from {reservation.deposit_amount}')


def stops_checking_func(reservation_form_pickup_dropoff_info_only_service_type, reservation, request, ):
    if int(reservation_form_pickup_dropoff_info_only_service_type[
               'stops_between_ride'].value()) != reservation.stops_between_ride:
        reservation.stops_address.all().delete()
        adding_stops = adding_stops_to_geo_address(request, reservation)
    else:
        check_if_stops_addresses_are_same_or_changed = check_stops_addresses_are_same_or_changed(
            request, reservation)
        if check_if_stops_addresses_are_same_or_changed:
            reservation.stops_address.all().delete()
            adding_stops = adding_stops_to_geo_address(request, reservation)
