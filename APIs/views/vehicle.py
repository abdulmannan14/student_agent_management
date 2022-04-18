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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_vehicle(request):
    try:
        company = request.user.userprofile.companyprofilemodel
    except:
        company = request.user.userprofile.personalclientprofilemodel.company
    vehicle = vehicle_models.Vehicle.objects.filter(company=company)
    serializer = vehicle_serializers.VehicleSerializer(vehicle, many=True)
    serializer_data = serializer.data
    if serializer_data:
        return Response(lc_utils.success_response(data=serializer_data))
    return Response(lc_utils.failure_response(msg="No record found!"))
