from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializer import *
from .models import *
from limoucloud_backend.utils import *


@api_view(['POST'])
def employee_register(request):
    if request.method == 'POST':
        try:
            employee_serializer = EmployeeSerializer(data=request.data)
            employee_address_serializer = EmployeeAddressSerializer(data=request.data)
            employee_profile_serializer = EmployeeProfileSerializer(data=request.data)
            if employee_serializer.is_valid() and employee_profile_serializer.is_valid() and employee_address_serializer.is_valid():
                employee = employee_serializer.save()
                employee.set_password(request.data['password'])
                employee.save()
                employee_address = employee_address_serializer.save()
                employee_profile = employee_profile_serializer.save()
                employee_profile.user = employee
                employee_profile.address = employee_address
                employee_profile.save()
                return Response(
                    success_response(employee_profile_serializer.data, 'Employee Successfully Register!'),
                    status=status.HTTP_200_OK
                )
            else:
                error = {}
                error.update(employee_serializer.errors)
                error.update(employee_profile_serializer.errors)
                error.update(employee_address_serializer.errors)
                return Response(failure_response(error, 'Resolve these error!'))
        except:
            return Response(failure_response('Something went wrong!'))
    else:
        return Response(
            failure_response('Something went Wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_employee(request):
    if request.method == 'GET':
        try:
            employee_profile = EmployeeProfileModel.objects.all()

            employee_profile_serializer = EmployeeProfileSerializer(employee_profile, many=True)
            if employee_profile:
                return Response(
                    success_response(employee_profile_serializer.data, 'Employee List!'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(success_response(employee_profile_serializer.data, 'No Employee found!'))
        except:
            return Response(failure_response('Something went wrong!'))
    else:
        return Response(
            failure_response('Something went wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
def edit_employee(request, pk):
    if request.method == 'PUT':
        employee_profile = get_object_or_404(EmployeeProfileModel, pk=pk)
        try:
            employee_serializer = EmployeeSerializer(data=request.data, instance=employee_profile.user)
            employee_profile_serializer = EmployeeProfileSerializer(data=request.data, instance=employee_profile)
            employee_address_serializer = EmployeeAddressSerializer(data=request.data,
                                                                    instance=employee_profile.address)
            if employee_serializer.is_valid() and employee_profile_serializer.is_valid() and employee_address_serializer.is_valid():
                employee_serializer.save()
                employee_profile_serializer.save()
                employee_address_serializer.save()
                return Response(
                    success_response(employee_profile_serializer.data, 'Employee Successfully Updated!'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(failure_response(employee_profile_serializer.errors, 'Remove this error below!'))
        except:
            return Response(failure_response('Something went wrong!'))
    else:
        return Response(
            failure_response('Something went Wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
def delete_employee(request, pk):
    if request.method == 'PUT':
        employee_profile = get_object_or_404(EmployeeProfileModel, pk=pk)
        try:
            employee_profile.address.delete()
            employee_profile.user.delete()
            return Response(success_response('Employee Delete Successfully!'))
        except:
            return Response(failure_response('Something went wrong!'))
    else:
        return Response(
            failure_response('Something went Wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )
