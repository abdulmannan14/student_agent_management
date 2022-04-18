from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from Company.models import CompanyProfileModel
from Company.serializers.CompanyAddressSerializer import CompanyAddressSerializer
from Company.serializers.CompanyLoginSerializer import CompanyLoginSerializer


class CompanyProfileSerializer(serializers.ModelSerializer):
    address = CompanyAddressSerializer(read_only=True)
    company = CompanyLoginSerializer(read_only=True)

    class Meta:
        model = CompanyProfileModel
        fields = '__all__'
        # depth = 2
