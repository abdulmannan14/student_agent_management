import base64

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from Account import models as account_models, utils as account_utils, account as account_account
from rest_framework.authtoken.models import Token
from Account.api_views.user_auth import serializers as user_auth_serializers
from limoucloud_backend import utils as backend_utils

from limoucloud_backend.utils import success_response, failure_response
from Account.api_views.user_auth import serializers as account_user_auth_serializers
from Employee import models as employee_models


class LoginApi(APIView):
    serializer_class = account_user_auth_serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(serializer.validated_data, request)

    def on_valid_request_data(self, data, request):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            user_profile = account_models.UserProfile.objects.get_or_create(user=user)[0]
            user_role = user_profile.role
            if user_role == 'DRIVER':
                get_username = user_profile.user.username
                get_employee = employee_models.EmployeeProfileModel.objects.get(
                    userprofile__user__username=get_username)
                work_status = get_employee.is_active

            if user_profile.email_verified:
                if user_role == "DRIVER":
                    user_profile_serializer = account_user_auth_serializers.UserProfileSerializerForDriver(user_profile)
                    user_profile_serializer = user_profile_serializer.data
                    user_profile_serializer['is_active'] = work_status
                elif user_role == 'CLIENT':
                    user_profile_serializer = account_user_auth_serializers.UserProfileSerializerForClient(user_profile)
                    user_profile_serializer = user_profile_serializer.data
                else:
                    return Response(failure_response(msg="Not Valid profile"), 403)
                image = user_profile_serializer['image']
                image = '.{}'.format(image)
                try:
                    with open(image, 'rb') as img_f:
                        encoded_string = base64.b64encode(img_f.read())
                    user_profile_serializer['image'] = encoded_string
                except:
                    pass
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'token': token.key,
                    'user_profile': user_profile_serializer,
                }
                return Response(
                    success_response(status_code=status.HTTP_200_OK, data=response, msg='User Login Successfully'))
            else:
                # user_profile_serializer = user_auth_serializers.UserProfileSerializer(user_profile)
                if user_role == "DRIVER":
                    user_profile_serializer = account_user_auth_serializers.UserProfileSerializerForDriver(user_profile)
                    user_profile_serializer = user_profile_serializer.data
                    user_profile_serializer['is_active'] = work_status

                elif user_role == 'CLIENT':
                    user_profile_serializer = account_user_auth_serializers.UserProfileSerializerForClient(user_profile)
                    user_profile_serializer = user_profile_serializer.data
                else:
                    return Response(failure_response(msg="Not Valid profile"), 403)

            token, created = Token.objects.get_or_create(user=user)
            response = {
                'token': token.key,
                'user_profile': user_profile_serializer,
            }
            return Response(
                success_response(status_code=status.HTTP_400_BAD_REQUEST, data=response,
                                 msg='Email is not verified, Please verify your email'))

        return Response(failure_response(msg="User not found!"), status=403)


class LogoutApi(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        response = {
        }
        return Response(
            success_response(status_code=status.HTTP_200_OK, data=response, msg='User Logged out Successfully'))


class SendVerificationCode(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        requested_data = request.data
        serializer = account_user_auth_serializers.SendVerificationCode(data=requested_data)
        serializer.is_valid(raise_exception=True)
        email = requested_data.get('email')
        try:
            get_user = get_object_or_404(User, email=email)
            get_userprofile = get_user.userprofile
            context = {'first_name': get_user.first_name, 'code': get_userprofile.verification_code,
                       'username': get_user.username,
                       'message': 'enter the code in your app in order to'
                                  ' verify your email.'
                       }
            account_utils._thread_making(backend_utils.send_email, ["LimouCloud Password Reset", context, get_user])
            return Response(success_response(msg='Verification code has been sent successfully'))
        except:
            return Response(failure_response(msg='Email Not Found'))


class EmailVerify(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        requested_data = request.data
        username = request.user.username
        serializer = account_user_auth_serializers.EmailVerify(data=requested_data)
        serializer.is_valid(raise_exception=True)
        code = requested_data.get('code')
        user_profile = account_account.get_user_profile(username, code)
        if user_profile:
            user_profile.email_verified = True
            user_profile.verification_code = account_utils.random_digits()  # to change code immediately to avoid future attacks
            user_profile.save()

            return Response(success_response(msg="email verified successfully"))
        else:
            return Response(failure_response(msg="incorrect verification code"))


class VerifyResetPasswordCode(APIView):
    def post(self, request, email):
        requested_data = request.data
        serializer = user_auth_serializers.EmailVerify(data=requested_data)
        serializer.is_valid(raise_exception=True)
        code = requested_data.get('code')
        user_profile = account_account.get_user_profile(email=email, code=code)
        if user_profile:
            return Response(success_response(msg="code verified successfully"))
        else:
            return Response(failure_response(msg="invalid code"))


class CreateNewPassword(APIView):
    def post(self, request, code):
        requested_data = request.data
        serializer = account_user_auth_serializers.PasswordCreationSerializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        current_password = requested_data.get('current_password')
        new_password = requested_data.get('new_password')
        confirm_new_password = requested_data.get('confirm_new_password')
        try:
            user_profile = account_account.get_user_profile(code=code)
        except:
            return Response(failure_response(msg="no user with this verification code found"))
        if user_profile is not None:
            if user_profile.user.check_password(current_password):
                if new_password == confirm_new_password:
                    if current_password != new_password:
                        user_profile.user.set_password(new_password)
                        user_profile.verification_code = account_utils.random_digits()
                        user_profile.save()
                        user_profile.user.save()
                        return Response(success_response(msg="password changed Successfully"))
                    return Response(failure_response(msg="new and current password cannot be same"))
                return Response(failure_response(msg="new and confirm password does not matched"))
            return Response(failure_response(msg="current password does not matched"))
        return Response(failure_response(msg="no user with this verification code found"))


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        get_username = request.user.username
        user_profile = account_account.get_user_profile(username=get_username)
        requested_data = request.data
        serializer = account_user_auth_serializers.PasswordCreationSerializer(data=requested_data)
        serializer.is_valid(raise_exception=True)
        current_password = requested_data.get('current_password')
        new_password = requested_data.get('new_password')
        confirm_new_password = requested_data.get('confirm_new_password')
        if user_profile:
            if user_profile.user.check_password(current_password):
                if new_password == confirm_new_password:
                    if current_password != new_password:
                        user_profile.user.set_password(new_password)
                        user_profile.user.save()
                        return Response(success_response(msg="password changed Successfully"))
                    return Response(failure_response(msg="new and current password cannot be same"))
                return Response(failure_response(msg="new and confirm password does not matched"))
            return Response(failure_response(msg="current password does not matched"))
        return Response(failure_response(msg="no user with this verification code found"))


class EditProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        requested_data = request.data
        get_username = request.user.username
        user_profile = account_account.get_user_profile(username=get_username)
        name = requested_data.get('name')
        number = requested_data.get('number')
        email = requested_data.get('email')
        notification = requested_data.get('notifications')
        new_trips_notifications = requested_data.get('new_trips_notifications')
        location = requested_data.get('location')
        dark_mode = requested_data.get('dark_mode')
        if name or email or number or dark_mode or notification or new_trips_notifications or location:
            if name:
                user_profile.user.username = name
            if email:
                user_profile.user.email = email
            if number:
                user_profile.phone = number
            if notification:
                user_profile.config.notification = notification
            if new_trips_notifications:
                user_profile.config.new_trips_notifications = new_trips_notifications
            if location:
                user_profile.config.location = location
            if dark_mode:
                user_profile.config.dark_mode = dark_mode
            user_profile.config.save()
            user_profile.save()
            user_profile.user.save()
            return Response(success_response(msg="Profile Updated Successfully"))
        else:
            return Response(failure_response(msg="please enter some data to update profile"))

    def get(self, request):
        get_user = request.user
        get_username = get_user.username
        user_profile = account_account.get_user_profile(username=get_username)
        get_user_role = user_profile.role
        if get_user_role == 'DRIVER':
            serializer = account_user_auth_serializers.EditProfileSerializerForDriver(user_profile)
        if get_user_role == 'CLIENT':
            serializer = account_user_auth_serializers.EditProfileSerializerForClient(user_profile)
        return Response(success_response(data=serializer.data))
