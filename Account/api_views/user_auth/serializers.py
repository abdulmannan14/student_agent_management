from rest_framework.serializers import ModelSerializer
from Account import models as account_models
from rest_framework import serializers
from django.contrib.auth.models import User


class ConfigurationSerializerForDriver(serializers.ModelSerializer):
    class Meta:
        model = account_models.Configuration
        exclude = ('id',)


class ConfigurationSerializerForClient(serializers.ModelSerializer):
    class Meta:
        model = account_models.Configuration
        fields = (
            'dark_mode',
            'location',
            'notification',
        )


class LoginSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, error_messages={'required': 'password field is required'})
    username = serializers.CharField(required=True,
                                     error_messages={'required': 'username field is required'})

    class Meta:
        model = account_models.User
        fields = (
            'username',
            'password',
        )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email already registered to other account! ")
        return lower_email

    class Meta:
        model = account_models.User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        )


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = account_models.Address
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()

    class Meta:
        model = account_models.UserProfile
        fields = '__all__'


class SendVerificationCode(serializers.Serializer):
    email = serializers.EmailField(required=True)


class EmailVerify(serializers.Serializer):
    code = serializers.IntegerField(required=True)


class PasswordCreationSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=20, required=True)
    new_password = serializers.CharField(max_length=20, required=True)
    confirm_new_password = serializers.CharField(max_length=20, required=True)


class UserProfileSerializerForDriver(serializers.ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()
    config = ConfigurationSerializerForDriver()

    class Meta:
        model = account_models.UserProfile
        fields = '__all__'


class UserProfileSerializerForClient(serializers.ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()
    config = ConfigurationSerializerForClient()

    class Meta:
        model = account_models.UserProfile
        fields = "__all__"


class EditProfileSerializerForDriver(serializers.ModelSerializer):
    user = UserSerializer()
    config = ConfigurationSerializerForDriver()

    class Meta:
        model = account_models.UserProfile
        fields = (
            'user',
            'phone',
            'config',
        )


class EditProfileSerializerForClient(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()
    config = ConfigurationSerializerForClient()

    class Meta:
        model = account_models.UserProfile
        fields = (
            'user',
            'phone',
            'config',
            'address',
        )
