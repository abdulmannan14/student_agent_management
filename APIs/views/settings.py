from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.authentication import BaseAuthentication
from APIs import utils as api_utils

from Reservation.filters import ReservationFilter
from Reservation.models import Reservation
from Reservation.serializers import ReservationSerializer, ReservationUpdateSerializer
from Vehicle.serializer import VehicleSerializer
from limoucloud_backend import utils as lc_utils
from Driver import utils as driver_utils
from Vehicle import models as vehicle_models
from Vehicle import serializer as vehicle_serializers
from Vehicle import filters as vehicle_filters
from limoucloud_backend.utils import success_response
from setting import models as setting_models, serializers as setting_serializer
from limoucloud_backend.settings import google_api_key


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_service_types(request):
    try:
        company = request.user.userprofile.companyprofilemodel
    except:
        company = request.user.userprofile.personalclientprofilemodel.company
    service_types = setting_models.ServiceType.objects.filter(company=company)
    serializer = setting_serializer.ServiceTypeSerializer(service_types, many=True)
    serializer_data = serializer.data
    if serializer_data:
        return Response(lc_utils.success_response(data=serializer_data))
    return Response(lc_utils.failure_response(msg="No record found!"))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_airports(request):
    try:
        company = request.user.userprofile.companyprofilemodel
    except:
        company = request.user.userprofile.personalclientprofilemodel.company
    airports = setting_models.CompanyAirport.objects.filter(company=company)
    serializer = setting_serializer.AirportSerializer(airports, many=True)
    serializer_data = serializer.data
    if serializer_data:
        return Response(lc_utils.success_response(data=serializer_data))
    return Response(lc_utils.failure_response(msg="No record found!"))


@api_view(["POST"])
def get_google_key(request):
    return Response(lc_utils.success_response(data=google_api_key))
