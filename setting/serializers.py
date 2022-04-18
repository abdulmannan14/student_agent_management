from rest_framework import serializers
from setting import models as setting_models


class ServiceTypeSerializer(serializers.ModelSerializer):
    service_type = serializers.CharField(source='all_service_type_name.name')

    class Meta:
        model = setting_models.ServiceType
        # fields = ['']
        exclude = ['all_service_type_name']
        # depth=1


class AirportSerializer(serializers.ModelSerializer):
    airport_name = serializers.CharField(source='airport.name')
    class Meta:
        model = setting_models.CompanyAirport
        # fields = "__all__"
        exclude=['airport']
        # depth=1
