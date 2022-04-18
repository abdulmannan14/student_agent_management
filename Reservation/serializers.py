from rest_framework import serializers

from setting import models as setting_models
from Client.serializer import ClientSerializer, PersonalClientProfileSerializer
from Vehicle import models as vehicle_models
from .models import Reservation, GeoAddress
from Employee import serializer as employee_serializers


class AllVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehicle_models.GeneralVehicle
        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    all_vehicle_name = AllVehicleSerializer()
    name = serializers.ReadOnlyField()

    class Meta:
        model = vehicle_models.Vehicle
        # fields = "__all__"
        # fields = ["name", "id"]
        exclude = ["vehicle_type", "company", "driver"]


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = setting_models.VehicleType
        # fields = "__all__"
        exclude = ["company"]


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = setting_models.ServiceType
        exclude = ["company"]


class GeoAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoAddress
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    client = PersonalClientProfileSerializer()
    vehicle_type = VehicleTypeSerializer()
    service_type = ServiceTypeSerializer()
    vehicle = VehicleSerializer()
    driver = employee_serializers.EmployeeShortProfileSerializer()
    pickup_address = GeoAddressSerializer()
    destination_address = GeoAddressSerializer()

    class Meta:
        model = Reservation
        # fields = "__all__"
        exclude = ["company"]


class ReservationCreateSerializer(serializers.ModelSerializer):
    # pickup_address = GeoAddressSerializer()
    # destination_address = GeoAddressSerializer()

    class Meta:
        model = Reservation
        fields = ["vehicle_type", "service_type",
                  # "pickup_address", "destination_address",
                  "pick_up_date",
                  "pick_up_time", "passenger_quantity", "luggage_bags_quantity", "car_seats", "pay_by"]


class ReservationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        # fields = "__all__"
        exclude = ["company"]


class ReservationCollectPaymentSerializer(serializers.Serializer):
    pay_by = serializers.CharField(max_length=50, required=True, allow_null=False)
