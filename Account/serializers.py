from abc import ABC

from rest_framework.serializers import ModelSerializer

from Account.models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email already registered to other account! ")
        return lower_email

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        )


class UserProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class LoginSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, error_messages={'required': 'password field is required'})
    username = serializers.CharField(required=True,
                                     error_messages={'required': 'username field is required'})

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(write_only=True, required=True)
    # last_name = serializers.CharField(write_only=True, required=True)
    # email = serializers.EmailField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = ["phone", "image"]


class ProfileConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = "__all__"
