import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q, F
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from limoucloud_backend import utils as backend_utils
from limoucloud_backend.utils import success_response, failure_response
from Reservation.api_views import serializers as reservation_serializers
from limoucloud_backend.utils import get_user_profile
from Reservation import models as reservation_models, utils as reservation_utils, \
    calculate_fare as reservation_calculate_fare
from Employee import models as employee_models
from Company import models as company_models
from setting import models as setting_models
from limoucloud_backend.decorators import user_passes_test


class AllReservations(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        requested_data = request.query_params
        serializer = reservation_serializers.ResevationStatusSerializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        # requested_data = request.query_params
        get_username = request.user.username
        reservation_status = data['reservation_status']
        reservation_status = reservation_status.upper()
        user_profile = get_user_profile(username=get_username)
        if reservation_status:
            reservations = self.get_reservations(user_profile, reservation_status)
        if reservation_status == "ALL":
            reservations = self.get_reservations(user_profile)
        serializer = reservation_serializers.ReservationSerializer(reservations, many=True)
        return Response(success_response(data=serializer.data, status_code=status.HTTP_200_OK))

    def get_reservations(self, user_profile, reservation_status=None):
        name = user_profile.user.id
        if user_profile.role == 'DRIVER':
            get_employee_id = employee_models.EmployeeProfileModel.objects.get(userprofile__user_id=name)
            if reservation_status:
                reservations = reservation_models.Reservation.objects.filter(driver_id=get_employee_id,
                                                                             reservation_status=reservation_status)
            else:
                reservations = reservation_models.Reservation.objects.filter(driver_id=get_employee_id)

        if user_profile.role == 'CLIENT':

            if reservation_status:
                reservations = reservation_models.Reservation.objects.filter(client=name,
                                                                             reservation_status=reservation_status)
            else:
                reservations = reservation_models.Reservation.objects.filter(client=name)
        return reservations


class ServiceTypes(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        company = request.user.userprofile.personalclientprofilemodel.company
        service_types = setting_models.ServiceType.objects.filter(company=company)
        serializer = reservation_serializers.ServiceTypeSerializer(service_types, many=True)
        return Response(success_response(data=serializer.data, status_code=status.HTTP_200_OK))


class VehicleEstimates(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        requested_data = request.data
        serializer = reservation_serializers.VehicleEstimateForReservationSerializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        company = request.user.userprofile.personalclientprofilemodel.company
        service_type = data.get('service_type')
        service_type = service_type.title()
        pickup_latlong = data.get('pickup_latlong')
        dropoff_latlong = data.get('dropoff_latlong')
        fares = reservation_calculate_fare.calculate_fares_according_to_vehicle_types(company, service_type,
                                                                                      pickup_latlong,
                                                                                      dropoff_latlong)
        return Response(success_response(data=fares, status_code=status.HTTP_200_OK))


class VehicleTotalFare(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        requested_data = request.data
        serializer = reservation_serializers.VehicleTotalFareForReservationSerializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        company = request.user.userprofile.personalclientprofilemodel.company
        service_type = data.get('service_type')
        service_type = service_type.title()
        vehicle_type = data.get('vehicle_type')
        vehicle_type = vehicle_type.title()
        fare = float(data.get('fare'))
        stops = int(data.get('stops'))
        passenger = int(data.get('passenger'))
        luggage = int(data.get('luggage'))

        fares = reservation_calculate_fare.calculate_vehicle_final_fare(company, service_type,
                                                                        vehicle_type,
                                                                        fare, stops, passenger, luggage)
        return Response(success_response(data=fares, status_code=status.HTTP_200_OK))


class ReservationHistory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        requested_data = request.query_params
        serializer = reservation_serializers.ReservationTypeSerializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        reservation_type = data['type']
        reservation_type = reservation_type.lower()
        user = request.user
        client = user.userprofile.personalclientprofilemodel

        # reservations=[]
        if reservation_type and reservation_type == 'history':
            reservations = reservation_models.Reservation.objects.filter(
                Q(reservation_status__icontains="Completed") | Q(
                    reservation_status__icontains="Cancelled"), client=client)
        elif reservation_type and reservation_type == 'upcoming':
            reservations = reservation_models.Reservation.objects.filter(reservation_status__icontains="Scheduled",
                                                                         client=client)
        else:
            return Response("Please Enter 'type' in params  --  options: history , upcoming ")
        serializer = reservation_serializers.ReservationSerializer(reservations, many=True)
        return Response(success_response(data=serializer.data, status_code=status.HTTP_200_OK))


class ReservationConf(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        try:
            company = user.userprofile.companyprofilemodel
        except:
            company = user.userprofile.personalclientprofilemodel.company
        service_types = setting_models.ServiceType.objects.filter(company=company)
        service_types = list(service_type.all_service_type_name.name for service_type in service_types)
        vehicle_types = setting_models.VehicleType.objects.filter(company=company)
        vehicle_types = list(vehicle_type.all_vehicle_type_name.name for vehicle_type in vehicle_types)
        reservation_statuses = reservation_models.Reservation.status_types
        reservation_statuses = list(reservation_status[0] for reservation_status in reservation_statuses)
        pay_bys = reservation_models.Reservation.payment_type
        pay_bys = list(pay_by[0] for pay_by in pay_bys)
        context = {
            'service_type': service_types,
            'vehicle_type': vehicle_types,
            'reservation_statuses': reservation_statuses,
            'pay_by': pay_bys,
        }
        return JsonResponse(context)
