from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from . import models as vehicle_models
from Employee.serializer import EmployeeShortProfileSerializer


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = vehicle_models.Vehicle
        fields = "__all__"
        depth=1


class FluidSerializer(serializers.ModelSerializer):
    comments = serializers.CharField(max_length=1000, source='fluid_comments')

    class Meta:
        model = vehicle_models.Fluid
        # fields = "__all__"
        exclude = ('fluid_comments',)


class BrakeTyreSerializer(serializers.ModelSerializer):
    comments = serializers.CharField(max_length=1000, source='break_comments')

    class Meta:
        model = vehicle_models.BrakeTyre
        # fields = "__all__"
        exclude = ('break_comments',)


class LightSerializer(serializers.ModelSerializer):
    comments = serializers.CharField(max_length=1000, source='light_comments')

    class Meta:
        model = vehicle_models.Light
        # fields = "__all__"
        exclude = ('light_comments',)


class MiscSerializer(serializers.ModelSerializer):
    comments = serializers.CharField(max_length=1000, source='misc_comments')

    class Meta:
        model = vehicle_models.Misc
        # fields = "__all__"
        exclude = ('misc_comments',)


class ChecklistSerializer(serializers.ModelSerializer):
    driver = EmployeeShortProfileSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.IntegerField(write_only=True, required=True)
    check_list_title = serializers.CharField(read_only=True)
    fluids = FluidSerializer()
    lights = LightSerializer()
    brake_and_tyres = BrakeTyreSerializer()
    misc = MiscSerializer()

    class Meta:
        model = vehicle_models.Checklist
        fields = "__all__"
        # depth = 2
