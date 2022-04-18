from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from django.urls import reverse
from rest_framework.response import Response
from limoucloud_backend.utils import *
from Company.serializers.CompanySerializer import CompanySerializer
from Company.serializers.CompanyAddressSerializer import CompanyAddressSerializer
from Company.serializers.CompanyProfileSerializer import CompanyProfileSerializer


@api_view(['POST'])
def company_register(request):
    if request.method == 'POST':
        try:
            company_serializer = CompanySerializer(data=request.data)
            company_address_serializer = CompanyAddressSerializer(data=request.data)
            company_profile_serializer = CompanyProfileSerializer(data=request.data)
            is_company_valid = company_serializer.is_valid()
            is_company_profile_valid = company_profile_serializer.is_valid()
            is_company_address_valid = company_address_serializer.is_valid()
            if is_company_valid and is_company_address_valid and is_company_profile_valid:
                company = company_serializer.save()
                company.set_password(request.data['password'])
                company.save()
                address = company_address_serializer.save()
                company_profile = company_profile_serializer.save()
                company_profile.address = address
                company_profile.company = company
                company_profile.save()
                return Response(
                    success_response(company_profile_serializer.data, 'Company Successfully Registered'),
                    status=status.HTTP_201_CREATED
                )
            else:
                errors = {}
                errors.update(company_serializer.errors)
                errors.update(company_profile_serializer.errors)
                errors.update(company_address_serializer.errors)
                return Response(
                    failure_response(errors, 'Please fix the errors below')
                )
        except:
            return Response(failure_response({'error': 'Somethig Went Wrong'}, 'Something went wrong'))
    else:
        return Response(
            failure_response('Something went wrong'),
            status=status.HTTP_400_BAD_REQUEST)
