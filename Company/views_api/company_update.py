from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from django.urls import reverse
from rest_framework.response import Response
from limoucloud_backend.utils import *
from Company.models.CompanyProfileModel import CompanyProfileModel
from Company.serializers.CompanySerializer import CompanySerializer
from Company.serializers.CompanyAddressSerializer import CompanyAddressSerializer
from Company.serializers.CompanyProfileSerializer import CompanyProfileSerializer


@api_view(['PUT'])
def company_update(request, pk):
    if request.method == 'PUT':
        company_profile = get_object_or_404(CompanyProfileModel, pk=pk)
        try:
            company_serializer = CompanySerializer(data=request.data, instance=company_profile.userprofile)
            company_address_serializer = CompanyAddressSerializer(data=request.data, instance=company_profile.address)
            company_profile_serializer = CompanyProfileSerializer(data=request.data, instance=company_profile)
            is_company_valid = company_serializer.is_valid()
            is_company_profile_valid = company_profile_serializer.is_valid()
            is_company_address_valid = company_address_serializer.is_valid()
            if is_company_valid and is_company_address_valid and is_company_profile_valid:
                company_profile_serializer.save()
                company_serializer.save()
                company_address_serializer.save()
                return Response(
                    success_response(company_profile_serializer.data, 'Request Data Successfully Updated!'),
                    status=status.HTTP_200_OK
                )
            else:
                errors = {}
                errors.update(company_serializer.errors)
                errors.update(company_profile_serializer.errors)
                errors.update(company_address_serializer.errors)
                return Response(
                    failure_response(errors, 'Please Fix The Following Error!'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                failure_response('Something went wrong!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(
            failure_response('somthing went wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )
