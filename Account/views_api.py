from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import format_html
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Account.serializers import *
from Account.models import *
from limoucloud_backend.utils import *
from Account.utils import *
from limoucloud_backend.utils import _get_error_msg
from . import urls_api as api_urls
from . import urls as view_urls
from . import account
from . import utils as account_utils
from .api_views.user_auth.serializers import UserProfileSerializerForDriver, UserProfileSerializerForClient
from django.contrib.auth.decorators import user_passes_test
from limoucloud_backend import decorators as backend_decorators


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        user_profile = UserProfile.objects.create(user=user, verification_code=random_digits())
        context = {'first_name': user.first_name,
                   'code': user_profile.verification_code, 'username': user.username,
                   'message': 'Thank you for signing up to LimouCloud. As you are new to our system so we need to verify'
                              ' your email first. Either enter the code given above or click on the link given below to'
                              ' verify your email.', 'link': '#'}
        send_email('Welcome to LimouCloud', context, user)
        user_profile_serializer = UserProfileSerializer(user_profile)
        data = user_profile_serializer.data
        data.update({"redirect_url": view_urls.account_signup_step_2()})
        return Response(
            success_response_fe(data, 'User Registered Successfully'),
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            failure_response_fe(serializer.errors, msg=_get_error_msg(serializer.errors)),
            status=status.HTTP_200_OK
        )


@api_view(["GET"])
def send_verification_code(request, username):
    user = account.get_user(username)
    if user:
        user_profile = user.userprofile
        user_profile.verification_code = random_digits()
        user_profile.save()
        verify_email_url = view_urls.verify_email(user.username) + '?code=' + str(user_profile.verification_code)
        context = {'first_name': user.first_name, 'code': user_profile.verification_code, 'username': user.username,
                   'message': 'Either enter the code given above or click on the link given below to'
                              ' verify your email.',
                   'link': "{}://{}{}?client=web".format(request.scheme, request.get_host(), verify_email_url)}
        account_utils._thread_making(send_email, ["Welcome to LimouCloud", context, user])
        return redirect(view_urls.verify_email(user_username=user.username))
    return Response(failure_response_fe(errors={}, msg="Unable to send code!"))


@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    next = request.GET.get("next", "")
    if serializer.is_valid():
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            response = {
                # 'token': get_token(user),
                # 'user_profile': user_profile_serializer.data,
                'redirect_url': next if next else reverse("company-index")
            }
            login(request=request, user=user)
            return Response(success_response_fe(response, 'User Login Successfully'))



        else:
            return Response(data=failure_response_fe(errors={'user': ['Invalid Username/Password!']},
                                                     msg='Invalid username or password'),
                            status=200)
    else:
        return Response(failure_response_fe(serializer.errors, 'Solve following errors'))


@api_view(['GET'])
def verify_email(request, username, code):
    try:
        user_profile = account.get_user_profile(username, code)
        if user_profile.email_verified:
            message = 'Email already verified! Please Login to continue'
            redirect_url = "{}?success=true&message={}".format(reverse("account-login"), message)
            return Response(failure_response_fe({}, message).update({"data": {"redirect_url": redirect_url}}))
        else:
            user_profile.email_verified = True
            user_profile.verification_code = random_digits()  # to change code immediately to avoid future attacks
            user_profile.save()
            message = "Profile verified successfully! Please Login to continue"
            redirect_url = "{}?success=true&message={}".format(reverse("account-login"), message)
            return Response(success_response_fe({
                "redirect_url": redirect_url
            }, message))
    except UserProfile.DoesNotExist:
        return Response(failure_response_fe({}, 'Invalid information'))


@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email', '')
    if email:
        user_profile = account.get_user_profile(email=email)
        if user_profile:
            random_digit = random_digits()
            user_profile.verification_code = random_digit
            user_profile.save()
            verification_url = view_urls.reset_password(user_profile.user.username, user_profile.verification_code)
            host = "{}://{}".format(request.scheme, request.get_host())
            verification_url = host + verification_url
            context = {
                'message': f'Hello <strong>{user_profile.user.username}</strong> We have received a request to reset you password. Kindly enter the code <strong>{user_profile.verification_code}</strong> above or hit'
                           f' the  <a href="{verification_url}">link</a> to reset your password. If you have not requested it please ignore this '
                           'email',
            }
            try:
                # _thread_making(send_email, ["Welcome to LimouCloud", context, user])
                account_utils._thread_making(send_email, ['LimouCloud Password Reset', context, user_profile.user])
                return Response(success_response_fe({'username': user_profile.user.username,
                                                     "redirect_url": view_urls.reset_password_code(
                                                         user_profile.user.username)
                                                     },
                                                    'Please check your email for reset password'))
            except:
                return Response(failure_response_fe('Some Connection Problem Please Send Email Again'))
        else:
            message = "User with email does not exits!"
            return Response(failure_response_fe({'email': [message]}, msg=message))
    return Response(failure_response_fe({'email': ['This Field Is Required']}))


@api_view(['GET', 'POST'])
def confirm_reset_password_code(request, username, code=None):
    if request.method == "POST":
        code = request.data.get("code")
    if code:
        try:
            user_profile = account.get_user_profile(username, code)
            url = reverse('set-user-password', kwargs={'username': username, 'code': user_profile.verification_code})
            data = {
                'message': 'send POST request to following url',
                'url': url,
                'redirect_url': get_full_url(request, view_urls.reset_password(username, code))
            }
            return Response(success_response_fe(data, 'Please Enter Your Password'))
        except:
            return Response(failure_response_fe({'code': ['Incorrect Code!']}, 'Incorrect Code!'), status=200)
    return Response(failure_response_fe({'code': ['This field is required']}, 'code is required'), status=200)


@api_view(['POST'])
def set_user_password(request, username, code):
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    if password and password == confirm_password:
        try:
            user_profile = account.get_user_profile(username, code)
            user_profile.user.set_password(password)
            user_profile.user.save()
            user_profile.verification_code = random_digits()
            user_profile.save()
            message = "Password Reset Successfully!"
            redirect_url = "{}?success=true&message={}".format(view_urls.login_url(), message)
            return Response(success_response_fe({"redirect_url": redirect_url}, message))
        except:
            return Response(failure_response_fe(msg="Incorrect information provided",
                                                errors=['Invalid code provided']), 403)
    return Response(failure_response_fe({'password': ['This Field is Required']},
                                        msg="Password and Confirm password are different"))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    try:
        user_profile: UserProfile = request.user.userprofile
        user_serializer = UpdateUserSerializer(data=request.data, instance=request.user)
        user_profile_serializer = UpdateUserProfileSerializer(data=request.data, instance=user_profile)
        if user_serializer.is_valid() and user_profile_serializer.is_valid():
            user_serializer.save()
            user_profile_serializer.save()
            if user_profile.role == user_profile.DRIVER:
                user_profile_serializer = UserProfileSerializerForDriver(user_profile)
                return Response(success_response(status_code=200, data=user_profile_serializer.data,
                                                 msg="Profile Updated successfully!"))
            elif user_profile.role == user_profile.CLIENT:
                user_profile_serializer = UserProfileSerializerForClient(user_profile)
                return Response(success_response(status_code=200, data=user_profile_serializer.data,
                                                 msg="Profile updated successfully!"))
        else:
            return Response(failure_response(errors=user_serializer.errors))
    except:
        return Response(failure_response(msg="Something went wrong!"))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_settings(request):
    try:
        user_profile: UserProfile = request.user.userprofile
        if user_profile.role == user_profile.DRIVER:
            config = user_profile.config
            config_serializer = ProfileConfigSerializer(data=request.data, instance=config)
            if config_serializer.is_valid():
                config_serializer.save()
                return Response(success_response(data=config_serializer.data, msg="Privacy updated successfully!"))
            else:
                return Response(failure_response(errors=config_serializer.errors))
        else:
            return Response(failure_response(msg="Not allowed to update privacy!"))
    except:
        return Response(failure_response(msg="Something went wrong!"))
