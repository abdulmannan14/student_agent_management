from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.settings import api_settings

from Account.serializers import UserSerializer
from .models import *


class EmployeeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAddress
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message='email already exists!')], required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message='username already exists!')],
        required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        )


class EmployeeProfileSerializer(serializers.ModelSerializer):
    address = EmployeeAddressSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = EmployeeProfileModel
        fields = '__all__'
        depth = 2


class EmployeeShortProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfileModel
        fields = ['id', 'full_name', 'username', "email", "primary_phone", "secondary_phone"]


class EmployeeLogin(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    username = serializers.CharField(required=True, error_messages={'required': 'username field is required'})
    password = serializers.CharField(write_only=True, error_messages={'required': 'password field is required'})

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    class Meta:
        model = User
        fields = (
            'token',
            'username',
            'password'
        )
