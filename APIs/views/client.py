from django.http import JsonResponse
from django.urls import reverse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.authentication import BaseAuthentication
import stripe
import Client.models
import limoucloud_backend.settings
from APIs import utils as api_utils
from limoucloud_backend.decorators import user_passes_test
from limoucloud_backend import utils as backend_utils
from Reservation.filters import ReservationFilter
from Reservation.models import Reservation
from Reservation import serializers as reservation_serializers
from Vehicle.serializer import VehicleSerializer
from limoucloud_backend import utils as lc_utils
from Vehicle import models as vehicle_models
from limoucloud_backend.utils import success_response, failure_response
from Vehicle import serializer as vehicle_serializers
from Client import utils as client_utils, models as client_models, serializer as client_serializers
from Merchants.stripe.utils import create_payment_intent
from rest_framework import status
from django.contrib.auth.models import User
from Account.models import UserProfile, Configuration
from Account import utils as account_utils, account as account_account


@api_view(["POST"])
def register_client(request):
    requested_data = request.data
    serializer = client_serializers.ClientRegisterSerializer(data=requested_data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    username = data.get('username')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    password = data.get('password')
    confirm_password = request.data.get('confirm_password')
    if password == confirm_password:
        try:
            if User.objects.filter(email=email).first():
                msg = "Email Already Exists"
                return Response(failure_response(msg=msg, status_code=status.HTTP_400_BAD_REQUEST))
            if User.objects.filter(username=username).first():
                msg = "Username Already Exists"
                return Response(failure_response(msg=msg, status_code=status.HTTP_400_BAD_REQUEST))
            user_obj = User(username=username, email=email, first_name=first_name, last_name=last_name)
            user_obj.set_password(password)
            user_obj.save()

            user_profile = UserProfile.objects.create(user=user_obj, verification_code=account_utils.random_digits(),
                                                      email_verified=False,
                                                      role='CLIENT', phone=phone)
            user_profile.save()
            context = {
                'subject': 'Client has been Created Successfully !',
                'message': f' Thank you   <strong>{user_obj.username}</strong> ! your Client account has been Created e at <a href="https://qa.limoucloud.com/">LimouCloud</a>. '
                           f'You Need to verify your email to log in'
                           f' Your verification code  is: <strong>{user_profile.verification_code}</strong> <br> <br>'
                           f'<br> Thankyou!  '
                           f'<br> Limoucloud Team.', }
            account_utils._thread_making(backend_utils.send_email, ["Welcome to LimouCloud", context, user_obj])

            return Response(success_response(data="User Created Successfully", status_code=status.HTTP_201_CREATED))

        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(failure_response(msg="Passwords doesn't matched",
                                         status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION))


@api_view(['GET'])
def verify_email(request):
    requested_data = request.query_params
    username = requested_data['username']
    code = requested_data['code']
    try:
        user_profile = UserProfile.objects.get(user__username=username, verification_code=code)
        if user_profile.email_verified:
            message = 'Email already verified! Please Login to continue'
            redirect_url = "{}?success=true&message={}".format(reverse("account-login"), message)
            return Response(failure_response(msg=redirect_url))
        else:
            user_profile.email_verified = True
            user_profile.verification_code = account_utils.random_digits()  # to change code immediately to avoid future attacks
            user_profile.save()
            message = "Profile verified successfully! Please Login to continue"
            redirect_url = "{}?success=true&message={}".format(reverse("account-login"), message)
            return Response(success_response(msg=redirect_url))
    except UserProfile.DoesNotExist:
        return Response(failure_response(msg='Invalid information'))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@user_passes_test(client_utils.is_client)
def post_reservation(request):
    client: Client.models.PersonalClientProfileModel = client_utils.get_client(request.user)
    data = request.data
    reservation_serializer = reservation_serializers.ReservationCreateSerializer(data=data)
    pick_up_address_serializer = reservation_serializers.GeoAddressSerializer(data=data.get("pickup_address", {}))
    dropoff_address_serializer = reservation_serializers.GeoAddressSerializer(data=data.get("destination_address", {}))
    stop_address_serializer = reservation_serializers.GeoAddressSerializer(data=data.get("stops", {}), many=True)
    if reservation_serializer.is_valid() and pick_up_address_serializer.is_valid() and dropoff_address_serializer.is_valid() and stop_address_serializer.is_valid():
        stops_address = stop_address_serializer.save()
        pick_up_address = pick_up_address_serializer.save()
        dropoff_address = dropoff_address_serializer.save()
        reservation: Reservation = reservation_serializer.save(
            pickup_address=pick_up_address,
            destination_address=dropoff_address,
            client=client,
            company=client.company,
            stops_between_ride=len(stops_address),
            charge_by='DISTANCE RATE'
            )
        for stop in stops_address:
            reservation.stops_address.add(stop)
        return Response(lc_utils.success_response())
    else:
        reser_errors = reservation_serializer.errors
        print(reser_errors)
        return Response(lc_utils.failure_response())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@user_passes_test(client_utils.is_client)
def get_company_service_types(request):
    client: Client.models.PersonalClientProfileModel = client_utils.get_client(request.user)
    company = client.company


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@user_passes_test(client_utils.is_client)
def add_client_card(request):
    requested_data = request.data
    serializer = client_serializers.CardSerializer(data=requested_data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    client: Client.models.PersonalClientProfileModel = client_utils.get_client(request.user)
    card_holder_name = data.get('card_holder_name')
    card_number = data.get('card_number')
    exp_month = data.get('exp_month')
    exp_year = data.get('exp_year')
    cvc = data.get('cvc')
    if card_number and cvc and exp_year and exp_month:
        create_payment_method = stripe.PaymentMethod.create(
            type="card",
            billing_details={
                'name': card_holder_name,
            },
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc,
            },
        )
        if create_payment_method:
            payment_method_id = create_payment_method['id']
            if payment_method_id:
                if client.merchant_account and client.merchant_account.stripe_id:
                    stripe_customer_id = client.merchant_account.stripe_id
                else:
                    stripe_customer_id = client.create_stripe_merchant_account().stripe_id
                stripe.PaymentMethod.attach(payment_method_id, customer=client.merchant_account.stripe_id)
        return Response(create_payment_method)
    else:
        return Response("Enter :  Card number , cvc , expiry month , expiry year")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@user_passes_test(client_utils.is_client)
def get_client_cards(request):
    client: Client.models.PersonalClientProfileModel = client_utils.get_client(request.user)
    if not client.merchant_account or not client.merchant_account.stripe_id:
        client.create_stripe_merchant_account()
    cards = stripe.PaymentMethod.list(customer=client.merchant_account.stripe_id, type="card").get("data", [])
    query_set = []
    for card in cards:
        query_set.append({
            "pk": client.pk,
            "id": card.get("id", ""),
            "card_holder": card.get("billing_details", {}).get("name", ""),
            "card_no": "{}".format(card.get("card", {}).get("last4", "")),
            "expires_at": "{}/{}".format(card.get("card", {}).get("exp_month", ""),
                                         card.get("card", {}).get("exp_year", "")),
            "brand": card.get("card", {}).get("brand", ""),
            "customer_id": card.get("customer", "")
        })
    return Response(query_set)
