from django.db import models

# Create your models here.
from django.urls import reverse

from Client.models import PersonalClientProfileModel
from Employee.models import EmployeeProfileModel
from Vehicle.models import Vehicle
from Company import models as company_models
from Employee.models import EmployeeProfileModel
from setting import models as setting_models


class GeoAddress(models.Model):
    address = models.CharField(max_length=300, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=8, null=True, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=8, null=True, blank=True)

    def __str__(self):
        return self.address

    # @property
    # def formated_address(self):
    #     return "{}, {}, {}, {}, {}, {}, {}".format(self.street, self.city, self.state, self.country, self.zip)


def get_duration_choices(duration=24):
    choices = []
    for i in range(0, duration):
        option = "{} hrs".format(i)
        choices.append((option, option))
    return choices


def get_stops_choices(duration=8):
    choices = []
    for i in range(0, duration):
        option = "{} stops".format(i)
        choices.append((option, option))
    return choices


class Reservation(models.Model):
    WEDDING = "WEDDING"
    PARTY = "PARTY"
    OTHER = "OTHER"
    service_types = [
        (WEDDING, WEDDING),
        (PARTY, PARTY),
        (OTHER, OTHER)
    ]
    SEDAN = "SEDAN"
    SUV = "SUV"
    vehicle_types = [
        (SEDAN, SEDAN),
        (SUV, SUV),
    ]
    CASH = 'CASH'
    CREDIT_CARD = 'CREDIT CARD'
    INVOICE = 'INVOICE'
    payment_type = [
        (CASH, CASH),
        (CREDIT_CARD, CREDIT_CARD),
        (INVOICE, INVOICE)
    ]
    QUOTED = 'QUOTED'
    CONFIRMED = 'CONFIRMED'
    SCHEDULED = 'SCHEDULED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    REQUESTED = 'REQUESTED'
    PICKED_UP = 'PENDING - PICKED UP'
    DROPPED_OFF = 'PENDING - DROPPED OFF'
    status_types = [
        (QUOTED, QUOTED),
        (CONFIRMED, CONFIRMED),
        (SCHEDULED, SCHEDULED),
        (COMPLETED, COMPLETED),
        (CANCELLED, CANCELLED),
        (REQUESTED, REQUESTED),
        (PICKED_UP, PICKED_UP),
        (DROPPED_OFF, DROPPED_OFF)
    ]
    FLAT_RATE = "FLAT RATE"
    HOURLY_RATE = "HOURLY RATE"
    DISTANCE_RATE = "DISTANCE RATE"
    DAILY_RATE = "DAILY RATE"
    charge_by = [
        (FLAT_RATE, FLAT_RATE),
        (HOURLY_RATE, HOURLY_RATE),
        (DISTANCE_RATE, DISTANCE_RATE),
        (DAILY_RATE, DAILY_RATE),
    ]

    deposit_types = [
        (CASH, CASH),
        (CREDIT_CARD, CREDIT_CARD)
    ]
    company = models.ForeignKey(company_models.CompanyProfileModel, null=True, blank=True, on_delete=models.CASCADE)
    reservation_status = models.CharField(max_length=35, null=False, blank=False, choices=status_types, default=QUOTED)
    client = models.ForeignKey(PersonalClientProfileModel, null=True, blank=True, on_delete=models.SET_NULL)
    service_type = models.ForeignKey(setting_models.ServiceType, on_delete=models.SET_NULL, null=True, blank=True)
    sales_tax = models.ForeignKey('setting.SalesTax', on_delete=models.CASCADE, null=True, blank=True)
    charge_by = models.CharField(max_length=50, choices=charge_by, null=True, blank=True)
    pay_by = models.CharField(max_length=50, choices=payment_type, null=True, blank=True, default='CASH',
                              verbose_name='Payment Method')
    vehicle_type = models.ForeignKey(setting_models.VehicleType, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(EmployeeProfileModel, null=True, blank=True, on_delete=models.SET_NULL)
    accepted_by_driver = models.BooleanField(null=True, blank=True, default=False)
    pickup_address = models.ForeignKey(GeoAddress, on_delete=models.SET_NULL, related_name='pickup_address', null=True,
                                       blank=True)
    destination_address = models.ForeignKey(GeoAddress, on_delete=models.SET_NULL, related_name='destination_address',
                                            null=True, blank=True)
    # pickup_address = models.CharField(max_length=200, null=True, blank=True)
    # destination_address = models.CharField(max_length=200, null=True, blank=True)
    pick_up_date = models.DateField(blank=True, null=True)
    pick_up_time = models.TimeField(blank=True, null=True)
    distance_in_miles = models.FloatField(null=True, blank=True)
    distance_covered_in_ride = models.FloatField(null=True, blank=True)
    total_hours = models.CharField(max_length=10, null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    no_of_days = models.IntegerField(null=True, blank=True)
    # distance= models.ForeignKey(setting_models.Distance,on_delete=models.CASCADE,null=True,blank=True)
    rate_per_mile = models.IntegerField(null=True, blank=True)
    rate_per_day = models.IntegerField(null=True, blank=True)
    additional_passenger_charge = models.IntegerField(null=True, blank=True)
    additional_luggage_charge = models.IntegerField(null=True, blank=True)
    additional_stops_charge = models.IntegerField(null=True, blank=True)
    stops_between_ride = models.IntegerField(null=True, blank=True, default=0)
    stops_address = models.ManyToManyField(GeoAddress, blank=True)
    passenger_quantity = models.IntegerField(blank=True, null=True, default=1)
    luggage_bags_quantity = models.IntegerField(blank=True, null=True, default=0)
    car_seats = models.IntegerField(blank=True, null=True)
    client_notes = models.CharField(max_length=150, null=True, blank=True)
    driver_notes = models.CharField(max_length=200, blank=True, null=True)
    discount_percentage = models.FloatField(null=True, blank=True, max_length=100, default=0.0)
    gratuity_percentage = models.FloatField(null=True, blank=True, max_length=100, default=0.0)
    fuel_Surcharge_percentage = models.FloatField(null=True, blank=True, max_length=100, default=0.0)
    sales_tax_percentage = models.FloatField(null=True, blank=True, default=0)
    tolls = models.IntegerField(null=True, blank=True, default=0)
    meet_and_greet = models.IntegerField(null=True, blank=True, default=0)
    duration = models.CharField(max_length=10, choices=get_duration_choices(25), null=True, blank=True)
    base_fare = models.FloatField(blank=True, null=True)
    deposit_amount = models.FloatField(null=True, blank=True, default=0)
    deposit_type = models.CharField(max_length=100, choices=deposit_types, null=True, blank=True)
    balance_fare = models.FloatField(null=True, blank=True, default=0)
    balance_paid = models.BooleanField(null=True, blank=True, default=False)
    total_fare = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def reservation_edit_url(self):
        return reverse("company-edit-reservations", kwargs={'pk': self.pk})

    def reservation_delete_url(self):
        return reverse("company-delete-reservations", kwargs={'pk': self.pk})

    def __str__(self):
        return "{},   Vehicle:{},   Total Charges:{}".format(self.client, self.vehicle,
                                                             self.total_fare)

    @property
    def date_diff(self):
        return (self.to_date - self.from_date).days
