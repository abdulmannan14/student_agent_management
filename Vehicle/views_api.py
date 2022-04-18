from rest_framework.decorators import api_view
from rest_framework.response import Response
from limoucloud_backend.utils import *
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Vehicle
from .serializer import VehicleSerializer


@api_view(['POST'])
def vehicle_register(request):
    if request.method == 'POST':
        try:
            vehicle_serializer = VehicleSerializer(data=request.data)
            if vehicle_serializer.is_valid():
                vehicle = vehicle_serializer.save()
                return Response(
                    success_response(vehicle_serializer.data, 'New Vehicle Add Successfully!'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(failure_response(vehicle_serializer.errors, 'Resolve these error!'))
        except:
            return Response(failure_response('Something went wrong!'))
    else:
        return Response(
            failure_response('Bad Request Method'),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_vehicle(request):
    if request.method == 'GET':
        try:
            vehicle = Vehicle.objects.all()
            vehicle_serializer = VehicleSerializer(vehicle, many=True)
            if vehicle:
                return Response(
                    success_response(vehicle_serializer.data, 'Vehicle Data!'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    failure_response(vehicle_serializer.errors, 'Something went wrong!')
                )
        except:
            return Response(
                failure_response('Something went wrong!')
            )
    else:
        return Response(
            failure_response('Something went wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
def edit_vehicle(request, pk):
    if request.method == 'PUT':
        vehicle = get_object_or_404(Vehicle, pk=pk)
        try:
            vehicle_serializer = VehicleSerializer(data=request.data, instance=vehicle)
            if vehicle_serializer.is_valid():
                vehicle_serializer.save()
                return Response(
                    success_response(vehicle_serializer.data, 'Vehicle Edit/Update Successfully!'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    failure_response(vehicle_serializer.errors, 'Resolve these error!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(failure_response('Something went wrong!'))
    else:
        return Response(
            failure_response('Something went wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
def vehicle_delete(request, pk):
    if request.method == 'DELETE':
        vehicle = get_object_or_404(Vehicle, pk=pk)
        try:
            vehicle.delete()
            return Response(
                success_response('Vehicle Deleted Successfully!'),
                status=status.HTTP_200_OK
            )
        except:
            return Response(failure_response('Something went wrong!'))
    else:
        return Response(
            failure_response('Something went wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )
