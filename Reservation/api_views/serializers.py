from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from Reservation import models as reservation_models
from setting import models as setting_models


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = reservation_models.Reservation
        fields = "__all__"


class ServiceTypeSerializer(serializers.ModelSerializer):
    service_type = serializers.CharField(source='all_service_type_name.name')

    class Meta:
        model = setting_models.ServiceType
        fields = ['service_type', 'type', 'round_trip']


class ResevationStatusSerializer(serializers.Serializer):
    reservation_status = serializers.CharField(max_length=25, required=True)


class VehicleEstimateForReservationSerializer(serializers.Serializer):
    service_type = serializers.CharField(max_length=30, required=True)
    pickup_latlong = serializers.CharField(max_length=30, required=True)
    dropoff_latlong = serializers.CharField(max_length=30, required=True)


class VehicleTotalFareForReservationSerializer(serializers.Serializer):
    service_type = serializers.CharField(max_length=30, required=True)
    vehicle_type = serializers.CharField(max_length=30, required=True)
    fare = serializers.CharField(max_length=30, required=True)
    stops = serializers.CharField(max_length=30, required=True)
    passenger = serializers.CharField(max_length=30, required=True)
    luggage = serializers.CharField(max_length=30, required=True)


class ReservationTypeSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=15, required=True)
