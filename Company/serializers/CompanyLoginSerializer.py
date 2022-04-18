from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class CompanyLoginSerializer(ModelSerializer):
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
