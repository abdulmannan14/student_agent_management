from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from limoucloud_backend.utils import *


@api_view(['POST'])
def client_register(request):
    if request.method == 'POST':
        try:
            client_serializer = ClientSerializer(data=request.data)
            client_personal_profile_serializer = PersonalClientProfileSerializer(data=request.data)
            client_business_profile_serializer = BusinessClientProfileSerializer(data=request.data)
            client_address_serializer = ClientAddressSerializer(data=request.data)
            client_payment_serializer = ClientPaymentInfoSerializer(data=request.data)
            client_serializer_isvalid = client_serializer.is_valid()
            client_personal_profile_serializer_isvalid = client_personal_profile_serializer.is_valid()
            client_business_profile_serializer_isvalid = client_business_profile_serializer.is_valid()
            client_address_serializer_isvalid = client_address_serializer.is_valid()
            client_payment_serializer_isvalid = client_payment_serializer.is_valid()
            if client_serializer_isvalid and client_personal_profile_serializer_isvalid and \
                    client_business_profile_serializer_isvalid and client_address_serializer_isvalid \
                    and client_payment_serializer_isvalid:
                client = client_serializer.save()
                client.set_password(request.data['password'])
                client.save()
                business_client = client_business_profile_serializer.save()
                client_address = client_address_serializer.save()
                client_payment = client_payment_serializer.save()
                client_personal_profile = client_personal_profile_serializer.save()

                client_personal_profile.business_client = business_client
                client_personal_profile.client_address = client_address
                client_personal_profile.client_payment_info = client_payment
                client_personal_profile.save()

                return Response(
                    success_response(client_personal_profile_serializer.data, 'Client Successfully registered!'),
                    status=status.HTTP_200_OK
                )
            else:
                error = {}
                error.update(client_serializer.errors)
                error.update(client_business_profile_serializer.errors)
                error.update(client_address_serializer.errors)
                error.update(client_payment_serializer.errors)
                error.update(client_personal_profile_serializer.errors)
                return Response(
                    failure_response(error, 'Resolve Error Below!')
                )
        except Exception as e:
            return Response(
                failure_response(e,'Something went wrong!!!')
            )
    else:
        return Response(
            failure_response('Something went wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_client(request):
    if request.method == 'GET':
        try:
            client_personal_profile = PersonalClientProfileModel.objects.all()
            client_personal_profile_serializer = PersonalClientProfileSerializer(client_personal_profile, many=True)
            if client_personal_profile:
                data = [
                    client_personal_profile_serializer.data
                ]
                return Response(
                    success_response(data, 'Client Information!'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(failure_response(client_personal_profile_serializer.errors, 'Something Went Wrong!'))
        except:
            return Response(failure_response('Something went wrong!'))
    else:
        return Response(
            failure_response('Something went Wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['PUT'])
def update_client(request, pk):
    if request.method == 'PUT':
        client_personal_profile = get_object_or_404(PersonalClientProfileModel, pk=pk)
        try:
            client_serializer = ClientSerializer(data=request.data, instance=client_personal_profile.user)
            client_personal_profile_serializer = PersonalClientProfileSerializer(data=request.data,
                                                                                 instance=client_personal_profile)
            client_business_profile_serializer = BusinessClientProfileSerializer(data=request.data,
                                                                                 instance=client_personal_profile.business_client)
            client_address_serializer = ClientAddressSerializer(data=request.data,
                                                                instance=client_personal_profile.client_address)
            client_payment_serializer = ClientPaymentInfoSerializer(data=request.data,
                                                                    instance=client_personal_profile.client_payment_info)
            client_serializer_isvalid = client_serializer.is_valid()
            client_personal_profile_serializer_isvalid = client_personal_profile_serializer.is_valid()
            client_business_profile_serializer_isvalid = client_business_profile_serializer.is_valid()
            client_address_serializer_isvalid = client_address_serializer.is_valid()
            client_payment_serializer_isvalid = client_payment_serializer.is_valid()

            if client_serializer_isvalid and client_personal_profile_serializer_isvalid \
                    and client_business_profile_serializer_isvalid and client_address_serializer_isvalid \
                    and client_payment_serializer_isvalid:
                client_serializer.save()
                client_business_profile_serializer.save()
                client_address_serializer.save()
                client_payment_serializer.save()
                client_personal_profile_serializer.save()
                return Response(
                    success_response(client_personal_profile_serializer.data, 'Client Update Successfully!'),
                    status=status.HTTP_200_OK
                )
            else:
                error = {}
                error.update(client_serializer.errors)
                error.update(client_business_profile_serializer.errors)
                error.update(client_address_serializer.errors)
                error.update(client_payment_serializer.errors)
                error.update(client_personal_profile_serializer.errors)
                return Response(
                    failure_response(error, 'Resolve Error Below!')
                )
        except:
            return Response(failure_response('Something went wrong!'))
    else:
        return Response(
            failure_response('Something Went Wrong'),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
def delete_client(request, pk):
    if request.method == 'DELETE':
        client_personal_profile = get_object_or_404(PersonalClientProfileModel, pk=pk)
        try:
            client_personal_profile.client_address.delete()
            client_personal_profile.client_payment_info.delete()
            client_personal_profile.business_client.delete()
            client_personal_profile.user.delete()
            return Response(
                success_response('Client Delete Successfully!'),
                status=status.HTTP_200_OK
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
