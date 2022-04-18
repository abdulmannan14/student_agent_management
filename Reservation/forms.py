from django import forms
from rest_framework import validators

import setting.models
from limoucloud_backend.utils import get_vehicle_types
from . import models as reservation_models, utils as reservation_utils
from Client import models as client_models
from Employee import models as employee_models
from django.contrib.auth.models import User
from Account import models as account_models

charge_by = (
    ("ALL", "ALL"),
    ("FLAT RATE", "FLAT RATE"),
    ("DISTANCE RATE", "DISTANCE RATE"),
    ("HOURLY RATE", "HOURLY RATE"),
    ("DAILY RATE", "DAILY RATE"),
)
status_type = (
    ("ALL", "ALL"),
    ("QUOTED", "QUOTED"),
    ("REQUESTED", "REQUESTED"),
    ("SCHEDULED", "SCHEDULED"),
    ("CONFIRMED", "CONFIRMED"),
    ("CANCELLED", "CANCELLED"),
    ("COMPLETED", "COMPLETED"),
)
pay_by = (
    ("ALL", "ALL"),
    ('CASH', 'CASH'),
    ('CREDIT CARD', 'CREDIT CARD'),
    ('INVOICE', 'INVOICE'),
)


# stop_choices = (
#     ("1", "ALL"),
#     ('2', 'CASH'),
#     ('2', 'CREDIT CARD'),
#     ('3', 'INVOICE'),
# )


class DropdownForm(forms.Form):
    Charge_By = forms.ChoiceField(choices=charge_by)
    Status_Type = forms.ChoiceField(choices=status_type)
    Pay_By = forms.ChoiceField(choices=pay_by)
    Vehicle_Type = forms.ChoiceField()


class ClientForm(forms.ModelForm):
    class Meta:
        model = client_models.PersonalClientProfileModel
        fields = "__all__"


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = employee_models.EmployeeProfileModel
        fields = "__all__"


def stops_choices(stops=9):
    choices = []
    for i in range(0, stops):
        option = "{}".format(i)
        choices.append((option, option))
    return choices


class ReservationFormPickupDropoffInfo(forms.ModelForm):
    stops_between_ride = forms.ChoiceField(choices=stops_choices)
    pickup_address = forms.CharField(max_length=300)
    destination_address = forms.CharField(max_length=300)

    class Meta:
        model = reservation_models.Reservation
        fields = ['pickup_address', 'destination_address', 'stops_between_ride']


class ReservationFormPickupDropoffInfoOnlyServiceType(forms.ModelForm):
    stops_between_ride = forms.ChoiceField(choices=stops_choices)
    pickup_address = forms.CharField(max_length=300)
    destination_address = forms.CharField(max_length=300)
    pick_up_date = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    pick_up_time = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'time'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_type'].required = True

    class Meta:
        model = reservation_models.Reservation
        fields = ['service_type', 'reservation_status', 'pick_up_date', 'pick_up_time',
                  'passenger_quantity', 'luggage_bags_quantity', 'pickup_address', 'destination_address',
                  'stops_between_ride']
        widgets = {
            "pick_up_date": forms.DateInput(attrs={"type": "date"}),
            "pick_up_time": forms.TextInput(attrs={"type": "time"}),
            "service_type": forms.Select(attrs={"class": "calculate_fare"}),

        }


#
# class ReservationPickupDateTimePassengerLuggage(forms.ModelForm):
#     pick_up_date = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))
#     pick_up_time = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'time'}))
#
#     class Meta:
#         model = reservation_models.Reservation
#         fields = ['pick_up_date', 'pick_up_time',
#                   'passenger_quantity', 'luggage_bags_quantity']
#         widgets = {
#             "pick_up_date": forms.DateInput(attrs={"type": "date"}),
#             "pick_up_time": forms.TextInput(attrs={"type": "time"}),
#
#         }


class ReservationFormClientInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].required = True

    class Meta:
        model = reservation_models.Reservation
        fields = ['client', ]


class ReservationFormPickupDropoffInfoForPostRequest(forms.ModelForm):
    class Meta:
        model = reservation_models.Reservation
        fields = ['stops_between_ride', 'service_type']


class ReservationFormVehcleAndDriverInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle_type'].required = True
        # self.fields['vehicle'].required = True
        self.fields['driver'].required = True

    class Meta:
        model = reservation_models.Reservation
        fields = ['vehicle_type', 'vehicle', 'driver']


class ReservationFormClientAndDriverNotesInfo(forms.ModelForm):
    class Meta:
        model = reservation_models.Reservation
        fields = ['client_notes', 'driver_notes']


class ReservationFormChargeByInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['charge_by'].required = True
        self.fields['sales_tax'].required = True

    class Meta:
        model = reservation_models.Reservation
        fields = ['charge_by', 'sales_tax']


class ReservationFormStops(forms.ModelForm):
    class Meta:
        model = reservation_models.Reservation
        fields = ['stops_between_ride']


class ReservationFormChargeByHours(forms.ModelForm):
    duration = forms.ChoiceField(choices=reservation_models.get_duration_choices(25))
    duration.widget.attrs.update({'onchange': 'durfunc(this);'})

    class Meta:
        model = reservation_models.Reservation
        fields = ['duration', ]


class ReservationFormChargeByDays(forms.ModelForm):
    no_of_days = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    base_fare = forms.IntegerField(required=True, widget=forms.TextInput(
        attrs={'Placeholder': 'fare of total days', 'readonly': 'readonly'}))
    from_date = forms.DateField(required=True,
                                widget=forms.TextInput(attrs={'type': 'date', 'onchange': 'datefunc(this);'}))
    to_date = forms.DateField(required=True,
                              widget=forms.TextInput(attrs={'type': 'date', 'onchange': 'datefunc(this);'}))
    rate_per_day = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'onchange': 'datefunc(this);'}))

    class Meta:
        model = reservation_models.Reservation
        fields = ['from_date', 'to_date', 'no_of_days', 'rate_per_day', 'base_fare']


class ReservationFormChargeByFlatRate(forms.ModelForm):
    # base_fare = forms.IntegerField(required=True)

    class Meta:
        model = reservation_models.Reservation
        fields = ['duration', 'base_fare']


class ReservationFormChargeByDistance(forms.ModelForm):
    distance_in_miles = forms.IntegerField(required=True, widget=forms.TextInput(
        attrs={'keyup onchange': 'myfunc(this);', "type": "number"}))
    rate_per_mile = forms.IntegerField(required=True, widget=forms.TextInput(
        attrs={'keyup onchange': 'myfunc(this);', "type": "number"}))
    fare_amount = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    base_fare = forms.IntegerField(required=True)

    class Meta:
        model = reservation_models.Reservation
        fields = ['distance_in_miles', ]


class ReservationFormDepositAndPaybyInfo(forms.ModelForm):
    class Meta:
        model = reservation_models.Reservation
        fields = ['deposit_amount', 'pay_by']


class ReservationFormClientAndRideInfo(forms.ModelForm):
    class Meta:
        model = reservation_models.Reservation
        fields = ['deposit_amount', 'pay_by']


class ChargeByForm(forms.ModelForm):
    class Meta:
        model = reservation_models.Reservation
        fields = ['charge_by', ]


class ReservationFormGratuityFuelSurchargeInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReservationFormGratuityFuelSurchargeInfo, self).__init__(*args, **kwargs)
        self.fields['additional_passenger_charge'].label = "Additional Per Passenger Charge"
        self.fields['additional_luggage_charge'].label = "Additional Per Luggage Charge"
        self.fields['additional_stops_charge'].label = "Additional Per Stop Charge"
        self.fields['gratuity_percentage'].required = True
        self.fields['fuel_Surcharge_percentage'].required = True
        self.fields['discount_percentage'].required = True
        self.fields['sales_tax_percentage'].required = True
        self.fields['tolls'].required = True
        self.fields['meet_and_greet'].required = True
        self.fields['additional_stops_charge'].required = True
        self.fields['additional_luggage_charge'].required = True
        self.fields['additional_passenger_charge'].required = True
        self.fields['total_fare'].required = True
        self.fields['deposit_amount'].required = True
        self.fields['pay_by'].required = True
        self.fields['balance_fare'].required = True
        self.fields['deposit_type'].required = True
        self.fields['sales_tax_percentage'].widget.attrs['readonly'] = True

    class Meta:
        model = reservation_models.Reservation
        fields = ['additional_passenger_charge', 'additional_luggage_charge', 'additional_stops_charge',
                  'gratuity_percentage', 'fuel_Surcharge_percentage', 'discount_percentage',
                  'sales_tax_percentage', 'tolls', 'meet_and_greet',
                  'total_fare', 'deposit_amount', 'deposit_type', 'balance_fare',
                  'pay_by']


class ReservationFormGratuityFuelSurchargeInfoForEditReservation(forms.ModelForm):
    class Meta:
        model = reservation_models.Reservation
        fields = ['balance_paid', 'accepted_by_driver', 'gratuity_percentage', 'fuel_Surcharge_percentage',
                  'discount_percentage', 'sales_tax_percentage',
                  'tolls', 'meet_and_greet']


class VehicleForm(forms.ModelForm):
    class Meta:
        model = reservation_models.Reservation
        fields = (
            'vehicle',
            'driver'
        )


class GeoAddressFormPickup(forms.ModelForm):
    pickup_address = forms.CharField(max_length=300, required=True)
    destination_address = forms.CharField(max_length=300, required=True)

    class Meta:
        model = reservation_models.Reservation
        fields = (
            'pickup_address', 'destination_address'
        )


class AirportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AirportForm, self).__init__(*args, **kwargs)
        self.fields['airport'].required = False

    class Meta:
        model = setting.models.CompanyAirport
        fields = ['airport', ]


# class FullReservationForm(forms.ModelForm):
#     pickup_address=forms.CharField()
#     destination_address=forms.CharField()
#     class Meta:
#         model = reservation_models.Reservation
#         fields = ['reservation_status', 'client', 'service_type', 'charge_by', 'pay_by', 'vehicle_type', 'vehicle',
#                   'driver', 'accepted_by_driver', 'pickup_address', 'destination_address', 'pick_up_date',
#                   'pick_up_time', 'additional_passenger_charge', 'additional_luggage_charge', 'additional_stops_charge',
#                   'stops_between_ride', 'passenger_quantity', 'luggage_bags_quantity', 'client_notes', 'driver_notes',
#                   'discount_percentage', 'gratuity_percentage', 'fuel_Surcharge_percentage', 'sales_tax_percentage',
#                   'tolls', 'meet_and_greet', 'base_fare', 'deposit_amount']


class ClinetFormForFirstLastNameEmail(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    address = forms.CharField(max_length=200)
    primary_phone = forms.CharField(max_length=200)
    secondary_phone = forms.CharField(max_length=200, required=False)

    class Meta:
        fields = ['first_name', 'last_name', 'email', 'address', 'primary_phone', 'secondary_phone']

# class ClinetFormForAddress(forms.ModelForm):
#     class Meta:
#         model = account_models.UserProfile
#         fields = ['address', ]
#

# class ClinetFormForPrimarySecondaryNumber(forms.ModelForm):
#     class Meta:
#         model = client_models.PersonalClientProfileModel
#         fields = ['primary_phone', 'secondary_phone', ]
