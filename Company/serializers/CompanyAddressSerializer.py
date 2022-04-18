from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from Company.models.CompanyAddressModel import CompanyAddressModel


class CompanyAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAddressModel
        fields = '__all__'
