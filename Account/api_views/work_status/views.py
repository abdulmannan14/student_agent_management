from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from limoucloud_backend.utils import failure_response, success_response


class WorkStatus(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        if request.user.userprofile.employeeprofilemodel:
            get_work_status = request.user.userprofile.employeeprofilemodel.is_active
            return Response(
                success_response(data=get_work_status, msg="User Work Status", status_code=status.HTTP_200_OK))

        else:
            return Response(failure_response(msg="user should be employee to check work status",
                                             status_code=status.HTTP_400_BAD_REQUEST))

    def post(self, request):
        if request.user.userprofile.employeeprofilemodel:
            work_status = request.data.get('is_active', False) or request.data.get('work_status', False)
            work_status = True if work_status else False
            user_profile = request.user.userprofile.employeeprofilemodel
            user_profile.is_active = work_status
            user_profile.save()
            return Response(
                success_response(msg="User Work Status has been updated successfully to {}".format(work_status),
                                 status_code=status.HTTP_200_OK))
        else:
            return Response(failure_response(msg="user should be employee to update work status",
                                             status_code=status.HTTP_400_BAD_REQUEST))
