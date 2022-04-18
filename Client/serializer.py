from rest_framework.validators import UniqueValidator

from Account.serializers import UserProfileSerializer
from .models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class ClientPaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPaymentInfoModel
        fields = '__all__'


class ClientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAddressModel
        fields = '__all__'


class BusinessClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessClientProfileModel
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message='email already exists!')], required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message='username already exists!')], required=True)
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


class PersonalClientProfileSerializer(serializers.ModelSerializer):
    business_client = BusinessClientProfileSerializer(read_only=True)
    client_address = ClientAddressSerializer(read_only=True)
    # client_payment_info = ClientPaymentInfoSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    userprofile = UserProfileSerializer()

    class Meta:
        model = PersonalClientProfileModel
        exclude = ["client_payment_info", "company"]


class ClientLoginSerializer(serializers.ModelSerializer):
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


class ClientRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(max_length=15, min_length=8, required=True)
    confirm_password = serializers.CharField(max_length=15, min_length=8, required=True)
    first_name = serializers.CharField(max_length=20, required=True)
    last_name = serializers.CharField(max_length=20, required=True)
    phone = serializers.IntegerField(required=True)


class CardSerializer(serializers.Serializer):
    card_holder_name = serializers.CharField(max_length=25,required=True)
    card_number = serializers.CharField(max_length=16,min_length=16,required=True)
    exp_month = serializers.CharField(max_length=25,required=True)
    exp_year = serializers.CharField(max_length=25,required=True)
    cvc = serializers.CharField(max_length=3,min_length=3,required=True)