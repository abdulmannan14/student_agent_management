from django.db import models
from Company import models as company_models
from django_cryptography.fields import encrypt

from django.db import models
from Company import models as company_models
from datetime import date


# Create your models here.
class GeneralVehicleType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class VehicleType(models.Model):
    all_vehicle_type_name = models.ForeignKey(GeneralVehicleType, on_delete=models.SET_NULL, null=True, blank=True,
                                              verbose_name='Vehicle Types')
    max_passengers = models.IntegerField(choices=[(x, x) for x in range(1, 56)])
    max_luggage = models.IntegerField(choices=[(x, x) for x in range(1, 56)])
    image = models.ImageField(upload_to='images', null=True, blank=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.all_vehicle_type_name.name)


class GeneralServiceType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    Transfer = "TRANSFER(P2P)"
    Hourly_service = "Hourly service"
    Airport_Pickup = "Airport Pickup"
    Airport_Dropoff = "Airport Dropoff"
    service_types = [
        (Transfer, Transfer),
        (Hourly_service, Hourly_service),
        (Airport_Pickup, Airport_Pickup),
        (Airport_Dropoff, Airport_Dropoff),
    ]
    all_service_type_name = models.ForeignKey(GeneralServiceType, on_delete=models.SET_NULL, null=True, blank=True)
    # name = models.CharField(max_length=30, null=True, blank=True)
    type = models.CharField(max_length=50, choices=service_types, null=True, blank=True, verbose_name='Type')
    round_trip = models.BooleanField(default=False, null=True, blank=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.all_service_type_name)


def get_duration_choices(duration=24):
    choices = []
    for i in range(1, duration):
        option = "{} hrs".format(i)
        choices.append((option, option))
    return choices


def get_duration_choices_simple_int(duration=24):
    choices = []
    for i in range(1, duration):
        # option = "{} hrs".format(i)
        choices.append((i, i))
    return choices


class ServiceArea(models.Model):
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Service Area Name")

    def __str__(self):
        return self.name


#

class GeneralAirport(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, null=True, blank=True)

    def __str__(self):
        return self.name


class CompanyAirport(models.Model):
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True,
                                default=None)
    airport = models.ForeignKey(GeneralAirport, on_delete=models.SET_NULL, null=True, related_name="company_airport")

    # airport = models.ForeignKey(GeneralAirport, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    # name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.airport}'


class Hour(models.Model):
    rate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.rate)


class Distance(models.Model):
    price_per_mile_distance = models.FloatField(null=True, blank=True)
    minimum_price_distance = models.FloatField(null=True, blank=True)
    base_price_distance = models.FloatField(null=True, blank=True)

    # def __str__(self):
    #     return str(self.price_per_mile_distance)


class Zone(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


def get_zone_choices():
    zones = Zone.objects.all()
    choices = []
    for zone in zones:
        choices.append((zone, zone))
    return choices


class ZoneToZone(models.Model):
    from_zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, related_name='from_zone', null=True, blank=True)
    to_zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, related_name='to_zone', null=True, blank=True)
    price = models.FloatField(null=True, blank=True)


class AirportToServiceArea(models.Model):
    airport = models.ForeignKey("setting.CompanyAirport", on_delete=models.SET_NULL, null=True, blank=True)
    service_area = models.ForeignKey("setting.ServiceArea", on_delete=models.SET_NULL, null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    service_price_row = models.ForeignKey('setting.ServicePrice', on_delete=models.SET_NULL, null=True, blank=True)

    # company=models.ForeignKey(company_models.CompanyProfileModel,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.service_area.name


class ServicePrice(models.Model):
    FLAT_RATE = "FLAT RATE"
    HOURLY_RATE = "HOURLY RATE"
    DISTANCE_RATE = "DISTANCE RATE"
    ZONE_TO_ZONE_FLAT = "ZONE TO ZONE FLAT"
    charge_by = [
        (FLAT_RATE, FLAT_RATE),
        (HOURLY_RATE, HOURLY_RATE),
        (DISTANCE_RATE, DISTANCE_RATE),
        (ZONE_TO_ZONE_FLAT, ZONE_TO_ZONE_FLAT),
    ]
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    sales_tax = models.ForeignKey('setting.SalesTax', on_delete=models.CASCADE, null=True, blank=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True, blank=True)
    price_type = models.CharField(max_length=30, choices=charge_by, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    gratuity_percentage = models.FloatField(null=True, blank=True, max_length=100, default=0.0)
    flat_rate = models.ManyToManyField(AirportToServiceArea, blank=True)
    distance_rate = models.ForeignKey(Distance, on_delete=models.SET_NULL, null=True, blank=True)
    hourly_rate = models.ManyToManyField(Hour, blank=True)
    zone_to_zone_rate = models.ManyToManyField(ZoneToZone, blank=True)
    minimum_hours = models.CharField(max_length=100, choices=get_duration_choices_simple_int(), null=True, blank=True)
    fuel_Surcharge_percentage = models.FloatField(null=True, blank=True, max_length=100, default=0.0)
    sales_tax_percentage = models.FloatField(null=True, blank=True, max_length=100, default=0.0)
    discount_percentage = models.FloatField(null=True, blank=True, max_length=100, default=0.0)
    tolls = models.IntegerField(null=True, blank=True, default=0)
    meet_and_greet = models.IntegerField(null=True, blank=True, default=0)
    per_additional_passenger = models.IntegerField(null=True, blank=True, default=0)
    per_additional_luggage = models.IntegerField(null=True, blank=True, default=0)
    per_additional_stop = models.IntegerField(null=True, blank=True, default=0)


class StripePayment(models.Model):
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    publish_key = models.CharField(max_length=256, null=True, blank=True)
    secret_key = encrypt(models.CharField(max_length=256, null=True, blank=True))
    account_id = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True, default=True)


class Feedback(models.Model):
    full_name = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(blank=True, null=True, verbose_name="How can we help ?")


class SalesTax(models.Model):
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    abbreviation = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    tax_number = models.CharField(max_length=50, null=True, blank=True)
    show_on_invoice = models.BooleanField(default=False, null=True, blank=True)
    recoverable = models.BooleanField(default=False, null=True, blank=True)
    compound = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class TaxRate(models.Model):
    # company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
    sales_tax = models.ForeignKey(SalesTax, on_delete=models.CASCADE, null=True)
    rate = models.FloatField(null=True, blank=True)
    effective_date = models.DateField(default=date(day=1, month=1, year=1900), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
