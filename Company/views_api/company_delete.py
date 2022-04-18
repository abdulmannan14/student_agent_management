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


@api_view(['DELETE'])
def company_delete(request, pk):
    if request.method == 'DELETE':
        company_profile = get_object_or_404(CompanyProfileModel, pk=pk)
        try:
            company_profile.address.delete()
            company_profile.company.delete()
            return Response(
                success_response('Company Deleted Successfully!'),
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                failure_response('Something went wrong!'),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return Response(
            failure_response('Something went wrong!'),
            status=status.HTTP_400_BAD_REQUEST
        )
