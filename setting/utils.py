from datetime import datetime
import stripe
from setting import models as setting_models
from pprint import pprint
from . import models as setting_models
from Company import models as company_models
from limoucloud_backend import settings


def get_hour_range():
    hour_range = []
    for i in range(1, 25):
        hour_range.append(i)
    return hour_range


def get_or_create_hours(service_price, max_hours):
    hours = service_price.hourly_rate.all()
    hours = list(hours)
    hours_counter = hours.__len__()
    for i in range(0, max_hours - hours_counter):
        hr = setting_models.Hour.objects.create(rate=0)
        service_price.hourly_rate.add(hr)
        hours.append(hr)
    service_price.save()
    return hours


def get_or_create_airport(airport, company, service_price_id):
    get_airport_name = setting_models.GeneralAirport.objects.get(id=airport)
    get_service_areas = setting_models.ServiceArea.objects.filter(company=company)
    get_service_areas_count = get_service_areas.count()
    check_availability = setting_models.AirportToServiceArea.objects.filter(airport=get_airport_name,
                                                                            service_price_row_id=service_price_id)
    check_availability_count = check_availability.count()
    if check_availability_count == get_service_areas_count:
        objects = check_availability
    else:
        for i in get_service_areas:
            objects = setting_models.AirportToServiceArea.objects.create(airport=get_airport_name, service_area=i,
                                                                         rate=0, service_price_row_id=service_price_id)
    return objects


def get_service_type(service_type):
    service_type_obj = setting_models.ServiceType.objects.get(id=service_type)
    return service_type_obj


def get_date_format(date):
    try:
        return "{}".format(date.strftime('%B-%d-%Y'))
    except:
        return date


def _get_company_dates(company):
    company_last_payment = get_date_format(company.company_package.started_at)
    company_due_payment = get_date_format(company.company_package.ends_at)
    member_since = get_date_format(company.created_at)
    return company_last_payment, company_due_payment, member_since


def _get_company_card_details(company):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    cards = stripe.PaymentMethod.list(customer=company.merchant_account.stripe_id, type="card").get("data", [])
    card_len = len(cards) - 1
    month = cards[card_len]['card']["exp_month"]
    datetime_object = datetime.strptime(str(month), "%m")
    month_name = datetime_object.strftime("%b")
    year = cards[card_len]['card']["exp_year"]
    type = cards[card_len]['card']["brand"]
    card_number = cards[card_len]['card']["last4"]
    return f"{month_name}-{year}", type, card_number
