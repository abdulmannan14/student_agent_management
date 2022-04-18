# Create your views here.
import json
from pprint import pprint

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from Accounting.DoubleEntry.models import ChartOfAccount
from Accounting.DoubleEntry.utils import journal_entry_reservation_add, journal_entry_reservation_edit
from limoucloud_backend import decorators as backend_decorators, utils as backend_utils
from django.contrib.auth.decorators import user_passes_test
from limoucloud_backend.utils import success_response_fe, failure_response_fe
from . import models as reservation_models, utils as reservation_utils, tables as reservation_tables, \
    forms as reservation_forms, serializers as reservation_serializers, calculate_fare as reservation_calculate_fare
from Company import models as company_models, utils as company_utils
from Vehicle import models as vehicle_models
from Client import models as client_models
from Employee import models as employee_models
from setting import models as setting_models, forms as setting_forms
from Company import urls as company_urls
from Account.utils import _thread_making
from Account import account as account_methods
from ast import literal_eval
from Home import models as home_models


@user_passes_test(backend_decorators._is_manager_or_dispatcher_or_company)
def all_reservation(request):
    try:
        company = request.user.userprofile.employeeprofilemodel.company
    except:
        company = request.user.userprofile.companyprofilemodel
    all_reservations = reservation_models.Reservation.objects.filter(company=company)
    charge_by = request.POST.get('Charge_By', None)
    status_type = request.POST.get('Status_Type', None)
    pay_by = request.POST.get('Pay_By', None)
    vehicle_type = request.POST.get('Vehicle_Type', None)
    reservations = reservation_utils.get_reservations(all_reservations, company, charge_by=charge_by,
                                                      pay_by=pay_by, status_type=status_type, vehicle_type=vehicle_type)
    get_types = backend_utils.get_my_company_vehicle_type(company=company)
    form = reservation_forms.DropdownForm()

    form.fields["Vehicle_Type"].choices = get_types
    table = reservation_tables.ReservationTables(reservations)
    sort = request.GET.get('sort', None)
    if sort:
        reservations = reservations.order_by(sort)
    context = {
        'links': [
            {
                'color_class': 'btn-primary',
                'title': 'New Reservation',
                'href': reverse('company-add-reservations'),
                'icon': 'fa fa-plus'
            },
        ],
        'button': 'submit',
        'filter_form': form,
        'page_title': 'Reservations',
        'subtitle': 'All the reservations are listed here',
        'table': table,
        'nav_bar': render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['reservations'],
        },
    }
    return render(request, 'dashboard/list-entries.html', context)


def add_reservation(request):
    user = request.user
    # try:
    #     company = user.userprofile.companyprofilemodel
    # except:
    #     company = user.userprofile.employeeprofilemodel.company
    if request.method == "POST":
        pass
        # # driver = request.POST.get('driver')
        # pickup_address_name = request.POST.get('pickup_address')
        # destination_address_name = request.POST.get('destination_address')
        # pickup_cordinates = request.POST.get('pickup_latlong')
        # destiantion_cordinates = request.POST.get('destination_latlong')
        # trip_address_split = reservation_utils.get_trip_cordinates(pickup_cordinates, destiantion_cordinates,
        #                                                            pickup_address_name, destination_address_name)
        # if not trip_address_split:
        #     return JsonResponse(failure_response_fe(msg="Please add valid pickup/drop off addresses!"))
        # adding_geo_for_pickup = trip_address_split[0]
        # adding_geo_for_destination = trip_address_split[1]
        #
        # # FORMS
        # reservation_form_pickup_dropoff_info_only_service_type = reservation_forms.ReservationFormPickupDropoffInfoOnlyServiceType(
        #     request.POST)
        # client_form = reservation_forms.ReservationFormClientInfo(request.POST)
        # reservation_form_vehicle_and_driver_info = reservation_forms.ReservationFormVehcleAndDriverInfo(request.POST)
        # reservation_form_client_and_driver_notes_info = reservation_forms.ReservationFormClientAndDriverNotesInfo(
        #     request.POST)
        # reservation_form_charge_by_info = reservation_forms.ReservationFormChargeByInfo(request.POST)
        # form1 = reservation_forms.ReservationFormGratuityFuelSurchargeInfo(request.POST)
        # airport_form = reservation_forms.AirportForm(request.POST)
        # FormForFirstLastNameEmail = reservation_forms.ClinetFormForFirstLastNameEmail()
        #
        # if client_form.is_valid() and reservation_form_vehicle_and_driver_info.is_valid() and reservation_form_client_and_driver_notes_info.is_valid() \
        #         and reservation_form_charge_by_info.is_valid() and form1.is_valid():
        #
        #
        #     # deposit_type = request.POST.get('deposit_payment')
        #     if form1.cleaned_data['deposit_amount'] > form1.cleaned_data['total_fare']:
        #         return JsonResponse(failure_response_fe(msg="Deposit amount cannot be greater than Total Fare amount"))
        #     if form1.cleaned_data['deposit_type'] == 'CREDIT CARD':
        #
        #         check_deposit_amount_and_transfer = reservation_utils.check_deposit_amount_and_transfer_funds(request,
        #                                                                                                       client_form.cleaned_data[
        #                                                                                                           'client'])
        #         if not check_deposit_amount_and_transfer.get("success"):
        #             return JsonResponse(check_deposit_amount_and_transfer)
        #     reservation = reservation_form_vehicle_and_driver_info.save(commit=False)
        #
        #     reservation.save()
        #     if form1.cleaned_data['deposit_amount'] == form1.cleaned_data['total_fare']:
        #         reservation.balance_paid = True
        #
        #     reservation_utils.adding_stops_to_geo_address(request, reservation)
        #     reservation_utils.saving_reservation_details(request, reservation, company,
        #                                                  adding_geo_for_pickup,
        #                                                  adding_geo_for_destination)
        #     reservation_utils.cals_acc_to_charge_type(reservation, request)
        #     reservation_utils.add_other_reservation_details(reservation, request)
        #     reservation_utils.sending_and_saving_email(reservation, request, company)
        #     journal_entry_reservation_add(reservation)
        #
        #     return JsonResponse(success_response_fe({"redirect_url": reverse("company-all-reservations")},
        #                                             msg='Reservation Created Successfully'))
        #
        #
        # else:
        #     return JsonResponse(failure_response_fe(msg="Form is not Validating, please check"))
    else:
        # sales_taxes=ChartOfAccount.object.filter(company=copnany)
        # Form for Client Section
        reservation_form_pickup_dropoff_info_only_service_type = reservation_forms.ReservationFormPickupDropoffInfoOnlyServiceType()
        # get_clients = client_models.PersonalClientProfileModel.objects.all()
        client_form = reservation_forms.ReservationFormClientInfo()
        # client_form.fields["client"].queryset = get_clients
        reservation_form_vehicle_and_driver_info = reservation_forms.ReservationFormVehcleAndDriverInfo()
        # vehicle_type = setting_models.VehicleType.objects.all()
        # reservation_form_vehicle_and_driver_info.fields['vehicle_type'].queryset = vehicle_type
        # driver = employee_models.EmployeeProfileModel.objects.all()
        # vehicle = vehicle_models.Vehicle.objects.none()
        # reservation_form_vehicle_and_driver_info.fields["driver"].queryset = driver
        # reservation_form_vehicle_and_driver_info.fields["vehicle"].queryset = vehicle
        reservation_form_client_and_driver_notes_info = reservation_forms.ReservationFormClientAndDriverNotesInfo()
        reservation_form_charge_by_info = reservation_forms.ReservationFormChargeByInfo()
        deposit_and_pay_by_form = reservation_forms.ReservationFormDepositAndPaybyInfo()
        form1 = reservation_forms.ReservationFormGratuityFuelSurchargeInfo()
        airport_form = reservation_forms.AirportForm()

        # company_airports = company.companyairport_set.all()
        # airport_form.fields['airport'].queryset = company_airports
        FormForFirstLastNameEmail = reservation_forms.ClinetFormForFirstLastNameEmail()

    context = reservation_utils.get_add_reservation_context(reservation_form_pickup_dropoff_info_only_service_type,
                                                            client_form, reservation_form_vehicle_and_driver_info,
                                                            reservation_form_client_and_driver_notes_info,
                                                            reservation_form_charge_by_info,
                                                            form1, FormForFirstLastNameEmail)

    return render(request, "company/reservation/create.html", context)


@user_passes_test(backend_decorators._is_company_or_manager)
def detail_reservation(request, pk):
    reservation = get_object_or_404(reservation_models.Reservation, pk=pk)
    user = request.user
    try:
        company = user.userprofile.companyprofilemodel
    except:
        company = user.userprofile.employeeprofilemodel.company
    reservation_form_pickup_dropoff_info_only_service_type = reservation_forms.ReservationFormPickupDropoffInfoOnlyServiceType(
        instance=reservation, initial={'pickup_address': reservation.pickup_address.address,
                                       'destination_address': reservation.destination_address})
    get_clients = client_models.PersonalClientProfileModel.objects.filter(company=company)
    client_form = reservation_forms.ReservationFormClientInfo(instance=reservation)
    client_form.fields["client"].queryset = get_clients
    reservation_form_vehicle_and_driver_info = reservation_forms.ReservationFormVehcleAndDriverInfo(
        instance=reservation)
    vehicle_type = setting_models.VehicleType.objects.filter(company=request.user.userprofile.companyprofilemodel)
    reservation_form_vehicle_and_driver_info.fields['vehicle_type'].queryset = vehicle_type
    driver = employee_models.EmployeeProfileModel.objects.filter(employee_role='Driver')
    vehicle = vehicle_models.Vehicle.objects.filter(company=company)
    reservation_form_vehicle_and_driver_info.fields["driver"].queryset = driver
    reservation_form_vehicle_and_driver_info.fields["vehicle"].queryset = vehicle
    reservation_form_client_and_driver_notes_info = reservation_forms.ReservationFormClientAndDriverNotesInfo(
        instance=reservation)
    reservation_form_charge_by_info = reservation_forms.ReservationFormChargeByInfo(instance=reservation)
    deposit_and_pay_by_form = reservation_forms.ReservationFormDepositAndPaybyInfo(instance=reservation)
    form1 = reservation_forms.ReservationFormGratuityFuelSurchargeInfo(instance=reservation,
                                                                       initial={
                                                                           'additional_passenger_charge': reservation.additional_passenger_charge,
                                                                           'additional_luggage_charge': reservation.additional_luggage_charge,
                                                                           'additional_stops_charge': reservation.additional_stops_charge,
                                                                           'gratuity_percentage': reservation.gratuity_percentage,
                                                                           'fuel_Surcharge_percentage': reservation.fuel_Surcharge_percentage,
                                                                           'discount_percentage': reservation.discount_percentage,
                                                                           'sales_tax_percentage': reservation.sales_tax_percentage,
                                                                           'tolls': reservation.tolls,
                                                                           'meet_and_greet': reservation.meet_and_greet,
                                                                           'deposit_amount': reservation.deposit_amount,
                                                                           'pay_by': reservation.pay_by,
                                                                           'total_fare': reservation.total_fare})
    airport_form = reservation_forms.AirportForm(instance=reservation)
    FormForFirstLastNameEmail = reservation_forms.ClinetFormForFirstLastNameEmail()

    context = reservation_utils.get_reservation_overview_context(reservation_form_pickup_dropoff_info_only_service_type,
                                                                 client_form, reservation_form_vehicle_and_driver_info,
                                                                 reservation_form_client_and_driver_notes_info,
                                                                 reservation_form_charge_by_info,
                                                                 form1, FormForFirstLastNameEmail, reservation)

    return render(request, "company/reservation/create.html", context)


def edit_reservation(request, pk):
    user = request.user
    try:
        company = user.userprofile.companyprofilemodel
    except:
        company = user.userprofile.employeeprofilemodel.company
    reservation = get_object_or_404(reservation_models.Reservation, pk=pk)

    if request.method == "POST":
        pickup_address_name = request.POST.get('pickup_address')
        destination_address_name = request.POST.get('destination_address')
        pickup_cordinates = request.POST.get('pickup_latlong')
        destiantion_cordinates = request.POST.get('destination_latlong')
        reservation_form_pickup_dropoff_info_only_service_type = reservation_forms.ReservationFormPickupDropoffInfoOnlyServiceType(
            request.POST, instance=reservation)
        client_form = reservation_forms.ReservationFormClientInfo(request.POST, instance=reservation)
        reservation_form_vehicle_and_driver_info = reservation_forms.ReservationFormVehcleAndDriverInfo(request.POST,
                                                                                                        instance=reservation)
        reservation_form_client_and_driver_notes_info = reservation_forms.ReservationFormClientAndDriverNotesInfo(
            request.POST, instance=reservation)
        reservation_form_charge_by_info = reservation_forms.ReservationFormChargeByInfo(request.POST,
                                                                                        instance=reservation)
        deposit_and_pay_by_form = reservation_forms.ReservationFormDepositAndPaybyInfo(request.POST,
                                                                                       instance=reservation)
        form1 = reservation_forms.ReservationFormGratuityFuelSurchargeInfo(request.POST, instance=reservation)
        airport_form = reservation_forms.AirportForm(request.POST, instance=reservation)
        FormForFirstLastNameEmail = reservation_forms.ClinetFormForFirstLastNameEmail()
        deposit_amount = reservation.deposit_amount
        if client_form.is_valid() and reservation_form_vehicle_and_driver_info.is_valid() and reservation_form_client_and_driver_notes_info.is_valid() \
                and reservation_form_charge_by_info.is_valid() and form1.is_valid():
            # deposit_type = request.POST.get('deposit_payment')
            if form1.cleaned_data['deposit_type'] == 'CREDIT CARD':
                check_deposit_amount_and_transfer = reservation_utils.for_edit_check_deposit_amount_and_transfer_funds(
                    request, client_form.cleaned_data['client'], reservation, deposit_amount)
                if not check_deposit_amount_and_transfer.get("success"):
                    return JsonResponse(check_deposit_amount_and_transfer)
            reservation_details = reservation_form_vehicle_and_driver_info.save(commit=False)
            reservation_details.save()
            if form1.cleaned_data['deposit_amount'] == form1.cleaned_data['total_fare']:
                reservation.balance_paid = True
            if request.POST.get('reservation_status') != reservation.reservation_status:
                sending_and_savings_emails = reservation_utils.sending_and_saving_email_for_client(reservation, request,
                                                                                                   company)
            if reservation_form_pickup_dropoff_info_only_service_type[
                'pickup_address'].value() == reservation.pickup_address.address and \
                    reservation_form_pickup_dropoff_info_only_service_type[
                        'destination_address'].value() == reservation.destination_address.address:
                adding_geo_for_pickup = reservation.pickup_address
                adding_geo_for_destination = reservation.destination_address
            else:
                trip_address_split = reservation_utils.get_trip_cordinates(pickup_cordinates, destiantion_cordinates,
                                                                           pickup_address_name,
                                                                           destination_address_name)
                adding_geo_for_pickup = trip_address_split[0]
                adding_geo_for_destination = trip_address_split[1]

            reservation_utils.cals_acc_to_charge_type(reservation, request)
            reservation_utils.stops_checking_func(
                reservation_form_pickup_dropoff_info_only_service_type, reservation, request)

            reservation_utils.saving_reservation_details(request, reservation, company,
                                                         adding_geo_for_pickup,
                                                         adding_geo_for_destination)
            reservation_utils.cals_acc_to_charge_type(reservation, request)
            reservation_utils.add_other_reservation_details(reservation, request)
            journal_entry_reservation_edit(reservation)

            return JsonResponse(success_response_fe({"redirect_url": reverse("company-all-reservations")},
                                                    msg='Reservation Edited Successfully'))

    else:
        reservation_form_pickup_dropoff_info_only_service_type = reservation_forms.ReservationFormPickupDropoffInfoOnlyServiceType(
            instance=reservation, initial={'pickup_address': reservation.pickup_address.address,
                                           'destination_address': reservation.destination_address})
        get_clients = client_models.PersonalClientProfileModel.objects.filter(company=company)
        client_form = reservation_forms.ReservationFormClientInfo(instance=reservation)
        client_form.fields["client"].queryset = get_clients
        reservation_form_vehicle_and_driver_info = reservation_forms.ReservationFormVehcleAndDriverInfo(
            instance=reservation)
        vehicle_type = setting_models.VehicleType.objects.filter(company=request.user.userprofile.companyprofilemodel)
        reservation_form_vehicle_and_driver_info.fields['vehicle_type'].queryset = vehicle_type
        driver = employee_models.EmployeeProfileModel.objects.filter(employee_role='Driver')
        vehicle = vehicle_models.Vehicle.objects.filter(company=company)
        reservation_form_vehicle_and_driver_info.fields["driver"].queryset = driver
        reservation_form_vehicle_and_driver_info.fields["vehicle"].queryset = vehicle
        reservation_form_client_and_driver_notes_info = reservation_forms.ReservationFormClientAndDriverNotesInfo(
            instance=reservation)
        reservation_form_charge_by_info = reservation_forms.ReservationFormChargeByInfo(instance=reservation, initial={
            'sales_tax': reservation.sales_tax})
        deposit_and_pay_by_form = reservation_forms.ReservationFormDepositAndPaybyInfo(instance=reservation)
        form1 = reservation_forms.ReservationFormGratuityFuelSurchargeInfo(instance=reservation, initial={
            'additional_passenger_charge': reservation.additional_passenger_charge,
            'additional_luggage_charge': reservation.additional_luggage_charge,
            'additional_stops_charge': reservation.additional_stops_charge,
            'gratuity_percentage': reservation.gratuity_percentage,
            'fuel_Surcharge_percentage': reservation.fuel_Surcharge_percentage,
            'discount_percentage': reservation.discount_percentage,
            'sales_tax_percentage': reservation.sales_tax_percentage,
            'tolls': reservation.tolls,
            'deposit_type': reservation.deposit_type,
            'meet_and_greet': reservation.meet_and_greet,
            'deposit_amount': reservation.deposit_amount,
            'pay_by': reservation.pay_by,
            'total_fare': reservation.total_fare})
        airport_form = reservation_forms.AirportForm(instance=reservation)
        FormForFirstLastNameEmail = reservation_forms.ClinetFormForFirstLastNameEmail()

        context = reservation_utils.get_add_reservation_context(reservation_form_pickup_dropoff_info_only_service_type,
                                                                client_form, reservation_form_vehicle_and_driver_info,
                                                                reservation_form_client_and_driver_notes_info,
                                                                reservation_form_charge_by_info,
                                                                form1, FormForFirstLastNameEmail,
                                                                reservation=reservation)

    return render(request, "company/reservation/create.html", context)


@user_passes_test(backend_decorators._is_company_or_manager)
@user_passes_test(backend_decorators._is_company_or_manager)
def delete_reservation(request, pk):
    company: company_models.CompanyProfileModel = company_utils.get_company_from_user(request.user)
    delete = backend_utils._delete_table_entry(reservation_models.Reservation, pk, company)
    return redirect('company-all-reservations')


def get_vehicle_type(request):
    vehicle_type = int(request.GET.get('vehicle_type', 0))
    get_vehicles_according_to_type = vehicle_models.Vehicle.objects.filter(
        vehicle_type_id=vehicle_type)
    serializer = reservation_serializers.VehicleSerializer(get_vehicles_according_to_type, many=True).data
    return JsonResponse(success_response_fe(serializer), safe=False)


def get_charge_type(request):
    reservation_id = request.GET.get('reservation_id', None)
    vehicle_type = request.GET.get('vehicle_type', '')
    service_type = request.GET.get('service_type', '')
    charge_by = request.GET.get('charge_by', '')
    try:
        reservation = get_object_or_404(reservation_models.Reservation, pk=reservation_id)
    except:
        reservation = None
    if charge_by == 'DISTANCE RATE':
        if charge_by and vehicle_type and service_type:
            try:
                if reservation:
                    rate_per_mile = reservation.rate_per_mile
                    tolls = reservation.tolls
                    meet_and_greet = reservation.meet_and_greet
                    gratuity_percentage = reservation.gratuity_percentage
                    fuel_surcharge_percentage = reservation.fuel_Surcharge_percentage
                    sales_tax_percentage = reservation.sales_tax_percentage
                    discount_percentage = reservation.discount_percentage
                    additional_passenger_charge = reservation.additional_passenger_charge
                    additional_luggage_charge = reservation.additional_luggage_charge
                    additional_stops_charge = reservation.additional_stops_charge
                    base_fare = reservation.base_fare
                    form = reservation_forms.ReservationFormChargeByDistance(
                        initial={"distance_in_miles": reservation.distance_in_miles,
                                 'fare_amount': ((reservation.distance_in_miles) * (reservation.rate_per_mile)),
                                 "rate_per_mile": reservation.rate_per_mile, "base_fare": reservation.base_fare})
                else:
                    get_service_price = setting_models.ServicePrice.objects.get(vehicle_type=vehicle_type,
                                                                                service_type=service_type,
                                                                                price_type=charge_by)
                    rate_per_mile = get_service_price.distance_rate.price_per_mile_distance
                    tolls = get_service_price.tolls
                    meet_and_greet = get_service_price.meet_and_greet
                    gratuity_percentage = get_service_price.gratuity_percentage
                    fuel_surcharge_percentage = get_service_price.fuel_Surcharge_percentage
                    sales_tax_percentage = get_service_price.sales_tax_percentage
                    discount_percentage = get_service_price.discount_percentage
                    additional_passenger_charge = get_service_price.per_additional_passenger
                    additional_luggage_charge = get_service_price.per_additional_luggage
                    additional_stops_charge = get_service_price.per_additional_stop
                    base_fare = get_service_price.distance_rate.base_price_distance
                    form = reservation_forms.ReservationFormChargeByDistance(
                        initial={"rate_per_mile": int(rate_per_mile),
                                 "base_fare": int(base_fare)})
                taxes = reservation_utils.get_taxes(tolls=tolls,
                                                    meet_and_greet=meet_and_greet,
                                                    gratuity_percentage=gratuity_percentage,
                                                    fuel_Surcharge_percentage=fuel_surcharge_percentage,
                                                    discount_percentage=discount_percentage,
                                                    additional_passenger_charge=additional_passenger_charge,
                                                    additional_luggage_charge=additional_luggage_charge,
                                                    additional_stops_charge=additional_stops_charge)
            except:
                if reservation:
                    form = reservation_forms.ReservationFormChargeByDistance(
                        initial={"distance_in_miles": reservation.distance_in_miles,
                                 'fare_amount': 0,
                                 "rate_per_mile": reservation.rate_per_mile, "base_fare": reservation.base_fare})
                else:
                    form = reservation_forms.ReservationFormChargeByDistance(
                    )
                taxes = reservation_utils.get_taxes(tolls=0,
                                                    meet_and_greet=0,
                                                    gratuity_percentage=0.0,
                                                    fuel_Surcharge_percentage=0.0,
                                                    sales_tax_percentage='',
                                                    discount_percentage=0.0,
                                                    additional_passenger_charge=0,
                                                    additional_luggage_charge=0,
                                                    additional_stops_charge=0)
        # else:
        #     if reservation:
        #         form = reservation_forms.ReservationFormChargeByDistance(
        #             initial={"distance_in_miles": reservation.distance_in_miles,
        #                      'fare_amount': ((reservation.distance_in_miles) * (reservation.rate_per_mile)),
        #                      "rate_per_mile": reservation.rate_per_mile, "base_fare": reservation.base_fare})
        #     else:
        #         form = reservation_forms.ReservationFormChargeByDistance(
        #         )
        #     taxes = ''


    elif charge_by == 'FLAT RATE':
        if charge_by and vehicle_type and service_type:
            try:
                get_service_price = setting_models.ServicePrice.objects.get(vehicle_type=vehicle_type,
                                                                            service_type=service_type,
                                                                            price_type=charge_by)
                prices = get_service_price.price
                if reservation:
                    rate_per_mile = reservation.rate_per_mile
                    tolls = reservation.tolls
                    meet_and_greet = reservation.meet_and_greet
                    gratuity_percentage = reservation.gratuity_percentage
                    fuel_surcharge_percentage = reservation.fuel_Surcharge_percentage
                    sales_tax_percentage = reservation.sales_tax_percentage
                    discount_percentage = reservation.discount_percentage
                    additional_passenger_charge = reservation.additional_passenger_charge
                    additional_luggage_charge = reservation.additional_luggage_charge
                    additional_stops_charge = reservation.additional_stops_charge
                    base_fare = reservation.base_fare
                    form = reservation_forms.ReservationFormChargeByFlatRate(initial=reservation.duration)
                else:
                    form = reservation_forms.ReservationFormChargeByFlatRate()
                    tolls = get_service_price.tolls
                    meet_and_greet = get_service_price.meet_and_greet
                    gratuity_percentage = get_service_price.gratuity_percentage
                    fuel_surcharge_percentage = get_service_price.fuel_Surcharge_percentage
                    sales_tax_percentage = get_service_price.sales_tax_percentage
                    discount_percentage = get_service_price.discount_percentage
                    additional_passenger_charge = get_service_price.per_additional_passenger
                    additional_luggage_charge = get_service_price.per_additional_luggage
                    additional_stops_charge = get_service_price.per_additional_stop
                taxes = reservation_utils.get_taxes(tolls=tolls,
                                                    meet_and_greet=meet_and_greet,
                                                    gratuity_percentage=gratuity_percentage,
                                                    fuel_Surcharge_percentage=fuel_surcharge_percentage,
                                                    sales_tax_percentage=sales_tax_percentage,
                                                    discount_percentage=discount_percentage,
                                                    additional_passenger_charge=additional_passenger_charge,
                                                    additional_luggage_charge=additional_luggage_charge,
                                                    additional_stops_charge=additional_stops_charge
                                                    )
            except:
                if reservation:
                    tolls = reservation.tolls
                    meet_and_greet = reservation.meet_and_greet
                    gratuity_percentage = reservation.gratuity_percentage
                    fuel_surcharge_percentage = reservation.fuel_Surcharge_percentage
                    sales_tax_percentage = reservation.sales_tax_percentage
                    discount_percentage = reservation.discount_percentage
                    additional_passenger_charge = reservation.additional_passenger_charge
                    additional_luggage_charge = reservation.additional_luggage_charge
                    additional_stops_charge = reservation.additional_stops_charge
                    base_fare = reservation.base_fare
                    deposit_amount = reservation.deposit_amount
                    form = reservation_forms.ReservationFormChargeByFlatRate(
                        initial={'duration': reservation.duration, 'base_fare': reservation.base_fare})
                    taxes = reservation_utils.get_taxes(tolls=tolls,
                                                        meet_and_greet=meet_and_greet,
                                                        gratuity_percentage=gratuity_percentage,
                                                        fuel_Surcharge_percentage=fuel_surcharge_percentage,
                                                        sales_tax_percentage=sales_tax_percentage,
                                                        discount_percentage=discount_percentage,
                                                        additional_passenger_charge=additional_passenger_charge,
                                                        additional_luggage_charge=additional_luggage_charge,
                                                        additional_stops_charge=additional_stops_charge
                                                        )

                else:
                    form = reservation_forms.ReservationFormChargeByFlatRate()
                    taxes = reservation_utils.get_taxes(tolls=0,
                                                        meet_and_greet=0,
                                                        gratuity_percentage=0.0,
                                                        fuel_Surcharge_percentage=0.0,
                                                        sales_tax_percentage='',
                                                        discount_percentage=0.0,
                                                        additional_passenger_charge=0,
                                                        additional_luggage_charge=0,
                                                        additional_stops_charge=0)
    elif charge_by == 'HOURLY RATE':
        if charge_by and vehicle_type and service_type:
            try:
                get_service_price = setting_models.ServicePrice.objects.get(vehicle_type=vehicle_type,
                                                                            service_type=service_type,
                                                                            price_type=charge_by)
                prices = get_service_price.hourly_rate.all()
                if reservation:
                    rate_per_mile = reservation.rate_per_mile
                    tolls = reservation.tolls
                    meet_and_greet = reservation.meet_and_greet
                    gratuity_percentage = reservation.gratuity_percentage
                    fuel_surcharge_percentage = reservation.fuel_Surcharge_percentage
                    sales_tax_percentage = reservation.sales_tax_percentage
                    discount_percentage = reservation.discount_percentage
                    additional_passenger_charge = reservation.additional_passenger_charge
                    additional_luggage_charge = reservation.additional_luggage_charge
                    additional_stops_charge = reservation.additional_stops_charge
                    base_fare = reservation.base_fare
                    form = reservation_forms.ReservationFormChargeByHours(initial=reservation.duration)
                else:
                    form = reservation_forms.ReservationFormChargeByHours()
                    tolls = get_service_price.tolls
                    meet_and_greet = get_service_price.meet_and_greet
                    gratuity_percentage = get_service_price.gratuity_percentage
                    fuel_surcharge_percentage = get_service_price.fuel_Surcharge_percentage
                    sales_tax_percentage = get_service_price.sales_tax_percentage
                    discount_percentage = get_service_price.discount_percentage
                    additional_passenger_charge = get_service_price.per_additional_passenger
                    additional_luggage_charge = get_service_price.per_additional_luggage
                    additional_stops_charge = get_service_price.per_additional_stop
                taxes = reservation_utils.get_taxes(tolls=tolls,
                                                    meet_and_greet=meet_and_greet,
                                                    gratuity_percentage=gratuity_percentage,
                                                    fuel_Surcharge_percentage=fuel_surcharge_percentage,
                                                    sales_tax_percentage=sales_tax_percentage,
                                                    discount_percentage=discount_percentage,
                                                    additional_passenger_charge=additional_passenger_charge,
                                                    additional_luggage_charge=additional_luggage_charge,
                                                    additional_stops_charge=additional_stops_charge
                                                    )
            except:
                if reservation:
                    tolls = reservation.tolls
                    meet_and_greet = reservation.meet_and_greet
                    gratuity_percentage = reservation.gratuity_percentage
                    fuel_surcharge_percentage = reservation.fuel_Surcharge_percentage
                    sales_tax_percentage = reservation.sales_tax_percentage
                    discount_percentage = reservation.discount_percentage
                    additional_passenger_charge = reservation.additional_passenger_charge
                    additional_luggage_charge = reservation.additional_luggage_charge
                    additional_stops_charge = reservation.additional_stops_charge
                    form = reservation_forms.ReservationFormChargeByHours(initial={'duration': reservation.duration})
                    taxes = reservation_utils.get_taxes(tolls=tolls,
                                                        meet_and_greet=meet_and_greet,
                                                        gratuity_percentage=gratuity_percentage,
                                                        fuel_Surcharge_percentage=fuel_surcharge_percentage,
                                                        sales_tax_percentage=sales_tax_percentage,
                                                        discount_percentage=discount_percentage,
                                                        additional_passenger_charge=additional_passenger_charge,
                                                        additional_luggage_charge=additional_luggage_charge,
                                                        additional_stops_charge=additional_stops_charge
                                                        )

                else:

                    form = reservation_forms.ReservationFormChargeByHours()
                    taxes = reservation_utils.get_taxes(tolls=0,
                                                        meet_and_greet=0,
                                                        gratuity_percentage=0.0,
                                                        fuel_Surcharge_percentage=0.0,
                                                        sales_tax_percentage='',
                                                        discount_percentage=0.0,
                                                        additional_passenger_charge=0,
                                                        additional_luggage_charge=0,
                                                        additional_stops_charge=0)
        # else:
        #     if reservation:
        #         form = reservation_forms.ReservationFormChargeByHours(initial=reservation.duration)
        #     else:
        #         form = reservation_forms.ReservationFormChargeByHours()
        #     taxes = reservation_utils.get_taxes(tolls=0,
        #                                         meet_and_greet=0,
        #                                         gratuity_percentage=0.0,
        #                                         fuel_Surcharge_percentage=0.0,
        #                                         sales_tax_percentage=0.0,
        #                                         discount_percentage=0.0,
        #                                         additional_passenger_charge=0,
        #                                         additional_luggage_charge=0,
        #                                         additional_stops_charge=0)
    elif charge_by == 'DAILY RATE':
        if reservation:
            tolls = reservation.tolls
            meet_and_greet = reservation.meet_and_greet
            gratuity_percentage = reservation.gratuity_percentage
            fuel_surcharge_percentage = reservation.fuel_Surcharge_percentage
            sales_tax_percentage = reservation.sales_tax_percentage
            discount_percentage = reservation.discount_percentage
            additional_passenger_charge = reservation.additional_passenger_charge
            additional_luggage_charge = reservation.additional_luggage_charge
            additional_stops_charge = reservation.additional_stops_charge
            form = reservation_forms.ReservationFormChargeByDays(
                initial={'base_fare': reservation.base_fare, 'from_date': reservation.from_date,
                         'to_date': reservation.to_date,
                         'no_of_days': reservation.no_of_days, 'rate_per_day': reservation.rate_per_day})
            taxes = reservation_utils.get_taxes(tolls=tolls,
                                                meet_and_greet=meet_and_greet,
                                                gratuity_percentage=gratuity_percentage,
                                                fuel_Surcharge_percentage=fuel_surcharge_percentage,
                                                sales_tax_percentage=sales_tax_percentage,
                                                discount_percentage=discount_percentage,
                                                additional_passenger_charge=additional_passenger_charge,
                                                additional_luggage_charge=additional_luggage_charge,
                                                additional_stops_charge=additional_stops_charge
                                                )

        else:
            form = reservation_forms.ReservationFormChargeByDays()
            taxes = reservation_utils.get_taxes(tolls=0,
                                                meet_and_greet=0,
                                                sales_tax_percentage='',
                                                gratuity_percentage=0.0,
                                                fuel_Surcharge_percentage=0.0,
                                                discount_percentage=0.0,
                                                additional_passenger_charge=0,
                                                additional_luggage_charge=0,
                                                additional_stops_charge=0)
    else:
        taxes = []
        return JsonResponse("charge type is not found", safe=False)
    try:
        context = {
            'charge_by_form': form,
            'prices': prices,

        }
    except:
        context = {
            'charge_by_form': form,

        }
    html = render_to_string("dashboard/type_form.html", context, request)
    response = success_response_fe(html)

    response["taxes"] = taxes
    return JsonResponse(response, safe=False)


def get_reservation_price_details(request):
    vehicle_type = request.GET.get('vehicle_type')
    service_type = request.GET.get('service_type')
    charge_by_type = request.GET.get('charge_by')
    try:
        get_service_price = setting_models.ServicePrice.objects.get(vehicle_type=vehicle_type,
                                                                    service_type=service_type,
                                                                    price_type=charge_by_type)
        if get_service_price.price_type == 'FLAT RATE':
            pass
        elif get_service_price.price_type == 'HOURLY RATE':
            prices = get_service_price.hourly_rate
            form = reservation_forms.ReservationFormChargeByHours()
            context = {
                'form': form
            }
        elif get_service_price.price_type == 'DISTANCE RATE':
            pass

        elif get_service_price.price_type == 'DAILY RATE':
            pass
        html = render_to_string("dashboard/type_form.html", context, request)
        return JsonResponse(success_response_fe(html), safe=False)

    except:
        pass


def get_airport_latlong(request):
    airport_name = request.GET.get('airport_name')
    airport = setting_models.GeneralAirport.objects.get(name=airport_name)
    lat_long = "{lat},{long}".format(lat=airport.latitude, long=airport.longitude)
    return JsonResponse(lat_long, safe=False)


def get_reservation_total_fare(request):
    fare = reservation_utils.calculate_reservation_fare_frontend(request)
    return JsonResponse(fare, safe=False)


def get_distance_in_miles(request):
    stop_1 = request.GET.get('stop_1', 0)
    stop_2 = request.GET.get('stop_2', 0)
    stop_3 = request.GET.get('stop_3', 0)
    stop_4 = request.GET.get('stop_4', 0)
    stop_5 = request.GET.get('stop_5', 0)
    stop_6 = request.GET.get('stop_6', 0)
    stop_7 = request.GET.get('stop_7', 0)
    stop_8 = request.GET.get('stop_8', 0)
    stops_between_ride = int(request.GET.get('stops_between_ride', 0))
    pickup_latlong = request.GET.get('pickup_latlong')
    destination_latlong = request.GET.get('destination_latlong')

    lat_longs = reservation_utils.get_lat_long(pickup_latlong, destination_latlong)
    addresses = [pickup_latlong, stop_1, stop_2, stop_3, stop_4, stop_5, stop_6, stop_7, stop_8, destination_latlong]
    if stops_between_ride > 0:
        distance = reservation_utils._get_total_distance_including_all_added_stops(addresses)
    else:
        distance = reservation_calculate_fare.calculate_distance(start_lat=lat_longs[0], start_lng=lat_longs[1],
                                                                 end_lat=lat_longs[2],
                                                                 end_lng=lat_longs[3])
    try:
        distance = distance.__round__(4)
    except:
        distance = distance
    return JsonResponse(distance, safe=False)


def get_company_airport(request):
    company = request.user.userprofile.companyprofilemodel
    airport = request.GET.get('airport', '')
    if airport:
        airport_obj = company.companyairport_set.filter(airport__name=airport).first()
        airport_latlong = '{lat},{lng}'.format(lat=airport_obj.airport.latitude, lng=airport_obj.airport.longitude)
        return JsonResponse(airport_latlong, safe=False)
    else:

        company_airports = company.companyairport_set.all()
        airports = []
        for airport in company_airports:
            airports.append(airport.airport.name)
        return JsonResponse(list(airports), safe=False)
