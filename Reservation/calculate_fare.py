import base64
from math import sin, cos, sqrt, atan2, radians
from setting import models as setting_models


def calculate_final_fare_without_taxes_and_extra_passengers_seats_luggage_and_stops(distance=None, rate_per_mile=None,
                                                                                    base_fare=None):
    fare = distance * rate_per_mile
    fare = fare + base_fare
    return fare


def calculate_distance(start_lat=None, start_lng=None, end_lat=None, end_lng=None):
    pickup_lat = radians(float(start_lat))
    pickup_long = radians(float(start_lng))
    dropoff_lat = radians(float(end_lat))
    dropoff_long = radians(float(end_lng))
    r = 6373.0
    dlon = dropoff_long - pickup_long
    dlat = dropoff_lat - pickup_lat
    a = sin(dlat / 2) ** 2 + cos(pickup_lat) * cos(dropoff_lat) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance_in_km = r * c
    conv_fac = 0.621371
    # calculate miles
    miles = distance_in_km * conv_fac
    return miles


def get_converted_latlong(pickup_latlong=None, dropoff_latlong=None):
    pickup_split = pickup_latlong.split(',')
    pickup_lat = pickup_split[0]
    pickup_lng = pickup_split[1]
    destination_split = dropoff_latlong.split(',')
    dropoff_lat = destination_split[0]
    dropoff_lng = destination_split[1]
    return pickup_lat, pickup_lng, dropoff_lat, dropoff_lng


def get_prices_for_reservation(vehicle_type=None, service_type=None, pickup_latlong=None, dropoff_latlong=None,
                               company=None):
    convert_latlong = get_converted_latlong(pickup_latlong=pickup_latlong, dropoff_latlong=dropoff_latlong)
    pickup_lat = convert_latlong[0]
    pickup_lng = convert_latlong[1]
    dropoff_lat = convert_latlong[2]
    dropoff_lng = convert_latlong[3]
    distance = calculate_distance(start_lat=pickup_lat, start_lng=pickup_lng, end_lat=dropoff_lat, end_lng=dropoff_lng)
    service_price_obj = setting_models.ServicePrice.objects.filter(company=company,
                                                                   service_type__all_service_type_name__name=service_type,
                                                                   vehicle_type=vehicle_type,
                                                                   price_type='DISTANCE RATE'
                                                                   ).last()
    try:
        rate_per_mile = service_price_obj.distance_rate.price_per_mile_distance
        base_fare = service_price_obj.distance_rate.base_price_distance
    except:
        rate_per_mile = 0
        base_fare = 0

    final_fare_without_taxes_and_extra_passengers_seats_luggage_and_stops = \
        calculate_final_fare_without_taxes_and_extra_passengers_seats_luggage_and_stops(
            distance=distance, rate_per_mile=rate_per_mile, base_fare=base_fare)
    return final_fare_without_taxes_and_extra_passengers_seats_luggage_and_stops


def calculate_fares_according_to_vehicle_types(company=None, service_type=None, pickup_latlong=None,
                                               dropoff_latlong=None):
    vehicle_types = setting_models.VehicleType.objects.filter(company=company)
    fares = []
    for vehicle_type in vehicle_types:
        final_price = get_prices_for_reservation(vehicle_type=vehicle_type, service_type=service_type,
                                                 pickup_latlong=pickup_latlong, dropoff_latlong=dropoff_latlong,
                                                 company=company)
        image = vehicle_type.image.url
        image = '.{}'.format(image)
        try:
            with open(image, 'rb') as img_f:
                encoded_string = base64.b64encode(img_f.read())
            vehicle_type.image = encoded_string
        except:
            pass
        data = {
            'vehicle_type': vehicle_type.all_vehicle_type_name.name,
            'image': vehicle_type.image,
            'max_passengers': vehicle_type.max_passengers,
            'max_luggage': vehicle_type.max_luggage,
            'fare': '$ {fare} USD'.format(fare=round(final_price, 3))
        }
        fares.append(data)
    return fares


def generate_total_fare_including_taxes_and_all(fare=None, stops=None,
                                                service_price_obj=None,
                                                vehicle_type_obj=None,
                                                passenger=None, luggage=None):
    base_fare = service_price_obj.distance_rate.base_price_distance
    fare_without_base_fare = fare - base_fare

    gratuity_percentage = service_price_obj.gratuity_percentage
    gratuity_value = (fare_without_base_fare / 100) * gratuity_percentage

    fuel_Surcharge_percentage = service_price_obj.fuel_Surcharge_percentage
    fuel_Surcharge_value = (fare_without_base_fare / 100) * fuel_Surcharge_percentage

    sales_tax_percentage = service_price_obj.sales_tax_percentage
    sales_tax_value = (fare_without_base_fare / 100) * sales_tax_percentage

    discount_percentage = service_price_obj.discount_percentage
    discount_value = (fare_without_base_fare / 100) * discount_percentage

    tolls = service_price_obj.tolls
    meet_and_greet = service_price_obj.meet_and_greet
    per_additional_stop = service_price_obj.per_additional_stop
    per_additional_luggage = service_price_obj.per_additional_luggage
    per_additional_passenger = service_price_obj.per_additional_passenger
    max_passengers = vehicle_type_obj.max_passengers
    max_luggage = vehicle_type_obj.max_luggage

    addition_passenger_fare = ((passenger - 1) * per_additional_passenger if passenger > max_passengers else 0)
    addition_luggage_fare = ((luggage - 1) * per_additional_luggage if luggage > max_luggage else 0)
    addition_stops_fare = (stops * per_additional_stop if stops > 0 else 0)

    total_fare = (fare_without_base_fare + gratuity_value + fuel_Surcharge_value + sales_tax_value + tolls + \
                  meet_and_greet + addition_passenger_fare + addition_luggage_fare + addition_stops_fare) - discount_value
    total_fare = total_fare
    fares = {
        'calculated_fare': fare_without_base_fare,
        'base_fare': base_fare,
        'taxes': {
            'gratuity_value': gratuity_value.__round__(2),
            'fuel_Surcharge_value': fuel_Surcharge_value.__round__(2),
            'sales_tax_value': sales_tax_value.__round__(2),
            'tolls': tolls,
            'meet_and_greet': meet_and_greet,
            'discount_value': discount_value.__round__(2),
            'addition_passenger_fare': addition_passenger_fare,
            'addition_luggage_fare': addition_luggage_fare,
            'addition_stops_fare': addition_stops_fare,
        },
        'total_fare': total_fare

    }
    return fares


def calculate_vehicle_final_fare(company=None, service_type=None, vehicle_type=None, fare=None, stops=None,
                                 passenger=None, luggage=None):
    vehicle_type_obj = setting_models.VehicleType.objects.get(company=company,
                                                              all_vehicle_type_name__name__contains=vehicle_type)

    service_price_obj = setting_models.ServicePrice.objects.filter(company=company,
                                                                   service_type__type=service_type,
                                                                   vehicle_type__all_vehicle_type_name__name=vehicle_type,
                                                                   price_type='DISTANCE RATE',
                                                                   ).last()
    total_fare = generate_total_fare_including_taxes_and_all(fare=fare, stops=stops,
                                                             service_price_obj=service_price_obj,
                                                             vehicle_type_obj=vehicle_type_obj,
                                                             passenger=passenger, luggage=luggage)
    return total_fare
