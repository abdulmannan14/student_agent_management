from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from django.urls import reverse
from rest_framework.response import Response
from limoucloud_backend.utils import *
from Company.models.CompanyProfileModel import CompanyProfileModel
from Company.serializers.CompanySerializer import CompanySerializer
from Company.serializers.CompanyAddressSerializer import CompanyAddressSerializer
from Company.serializers.CompanyProfileSerializer import CompanyProfileSerializer


@api_view(['GET'])
def get_company_list(request):
    if request.method == 'GET':
        try:
            company_profile = CompanyProfileModel.objects.all()
            company_profile_serializer = CompanyProfileSerializer(company_profile, many=True)
            if company_profile:
                data = [
                    company_profile_serializer.data
                ]
                return Response(
                    success_response(data, 'Operation Success'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    failure_response(company_profile_serializer.errors, 'Something Went Wrong'),
                )
        except:
            return Response(
                failure_response({}, 'Something went Wrong')
            )
    else:
        return Response(
            failure_response({}, 'Something Went Wrong'),
            status=status.HTTP_400_BAD_REQUEST
        )
