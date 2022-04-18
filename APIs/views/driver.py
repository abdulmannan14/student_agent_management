from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.authentication import BaseAuthentication
from APIs import utils as api_utils
from Merchants.stripe import utils as merchant_stripe_utils
from Reservation.filters import ReservationFilter
from Reservation.models import Reservation
from Reservation.serializers import ReservationSerializer, ReservationUpdateSerializer
from Reservation import serializers as reservation_serializers
from Vehicle.serializer import VehicleSerializer
from limoucloud_backend import utils as lc_utils
from Driver import utils as driver_utils
from Vehicle import models as vehicle_models
from Vehicle import serializer as vehicle_serializers
from Vehicle import filters as vehicle_filters


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def test(request):
    return Response(lc_utils.success_response())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_reservations(request):
    page_size = int(request.GET.get("page_size", 10))
    page_size = 10 if page_size < 1 else page_size
    driver = driver_utils.get_driver(user=request.user)
    status = request.GET.get("status", "")
    reservations = Reservation.objects.filter(driver=driver)
    if status and status.lower() == "new":
        reservations = reservations.filter(
            Q(reservation_status__icontains="confirmed") | Q(reservation_status__icontains="requested") |
            Q(reservation_status__icontains="scheduled")
        )
    elif status and status.lower() == "history":
        reservations = reservations.filter(
            Q(reservation_status__icontains="cancelled") | Q(reservation_status__icontains="completed")
        )
    reservations = ReservationFilter(request.GET, reservations)
    return api_utils.get_paginated_response(reservations.qs, request, ReservationSerializer, page_size)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_new_reservation_count(request):
    driver = driver_utils.get_driver(user=request.user)
    reservations = Reservation.objects.filter(driver=driver, reservation_status__icontains="requested")
    return Response(lc_utils.success_response(data={"count": len(reservations)}))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_vehicle_checklists_options(request):
    options = vehicle_models.get_checklist_options()
    _list = [option[0] for option in options]
    return Response(lc_utils.success_response(data={"checklist_options": _list}))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_a_reservation(request, pk):
    driver = driver_utils.get_driver(user=request.user)
    reservation = get_object_or_404(Reservation, pk=pk, driver=driver)
    serializer = ReservationSerializer(reservation)
    data = serializer.data
    if data:
        return Response(lc_utils.success_response(data=data))
    return Response(lc_utils.failure_response(msg="No record found!"))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_vehicle_checklists(request):
    page_size = int(request.GET.get("page_size", 10))
    page_size = 10 if page_size < 1 else page_size
    driver = driver_utils.get_driver(user=request.user)
    checklists = vehicle_models.Checklist.objects.filter(driver=driver)
    filters = vehicle_filters.ChecklistFilter(request.GET, checklists)
    return api_utils.get_paginated_response(filters.qs, request, vehicle_serializers.ChecklistSerializer, page_size)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_a_checklist(request, pk):
    driver = driver_utils.get_driver(user=request.user)
    checklist = get_object_or_404(vehicle_models.Checklist, pk=pk, driver=driver)
    serializer = vehicle_serializers.ChecklistSerializer(checklist)
    data = serializer.data
    if data:
        return Response(lc_utils.success_response(data=data))
    return Response(lc_utils.failure_response(msg="No record found!"))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_driver_assigned_vehicle(request):
    driver = driver_utils.get_driver(user=request.user)
    vehicle = driver.vehicle_set.last()
    if vehicle:
        return Response(lc_utils.success_response(data=VehicleSerializer(vehicle).data))
    return Response(lc_utils.failure_response(msg="No record found!"))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_checklist(request):
    driver = driver_utils.get_driver(user=request.user)
    if driver:
        data = request.data
        millage = data.get("vehicle_millage", "") or data.get("vehicle_milage", "")
        serializer = vehicle_serializers.ChecklistSerializer(data=request.data)
        fluid_serializer = vehicle_serializers.FluidSerializer(data=request.data.get("fluids", {}))
        brake_and_tyres_serializer = vehicle_serializers.BrakeTyreSerializer(
            data=request.data.get("brake_and_tyres", {}))
        lights_serializer = vehicle_serializers.LightSerializer(
            data=request.data.get("lights", {}))
        misc_serializer = vehicle_serializers.MiscSerializer(
            data=request.data.get("misc", {}))
        if serializer.is_valid() and fluid_serializer.is_valid() and brake_and_tyres_serializer.is_valid() \
                and lights_serializer.is_valid() and misc_serializer.is_valid():
            brake_and_tyres = brake_and_tyres_serializer.save()
            fluid = fluid_serializer.save()
            lights = lights_serializer.save()
            misc = misc_serializer.save()
            checklist = serializer.save(driver=driver, vehicle_id=request.data.get("vehicle_id", 0), fluids=fluid,
                                        brake_and_tyres=brake_and_tyres, lights=lights, misc=misc)
            checklist.vehicle.milage = millage
            checklist.vehicle.save()
            return Response(lc_utils.success_response(data=serializer.data))
        else:
            errors = brake_and_tyres_serializer.errors  # .update(brake_and_tyres_serializer.errors)
            return Response(lc_utils.failure_response(errors=errors, msg="Resolve the errors"))
    else:
        return Response(lc_utils.failure_response(msg="Please login as driver!"))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_reservation(request, pk):
    driver = driver_utils.get_driver(user=request.user)
    if driver:
        data = request.data
        reservation = get_object_or_404(Reservation, pk=pk)
        if driver != reservation.driver:
            return Response(lc_utils.failure_response(msg="You are not authorized for this action"))
        serializer = ReservationUpdateSerializer(instance=reservation, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(lc_utils.success_response(data=serializer.data, msg="Reservation updated successfully!"))
        else:
            return Response(lc_utils.failure_response(errors=serializer.errors))

    return Response(lc_utils.failure_response(msg="Please login as driver!"))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_reservation(request, pk):
    driver = driver_utils.get_driver(user=request.user)
    if driver:
        data = request.data
        is_accepted = data.get("is_accepted", None)
        if is_accepted is None:
            return Response(lc_utils.failure_response(errors={'is_accepted': ['This field is required']},
                                                      msg="is_active is required field!"))
        reservation = get_object_or_404(Reservation, pk=pk)
        if driver != reservation.driver:
            return Response(lc_utils.failure_response(msg="You are not authorized for this action"))
        status = reservation.CONFIRMED if is_accepted else reservation.CANCELLED
        reservation.accepted_by_driver = is_accepted
        reservation.reservation_status = status
        reservation.save(update_fields=["accepted_by_driver", "reservation_status"])
        return Response(lc_utils.success_response(msg="Reservation {} successfully!".format(status)))
    return Response(lc_utils.failure_response(msg="Please login as driver!"))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def collect_reservation_payment(request, pk):
    requested_data = request.data
    serializer = reservation_serializers.ReservationCollectPaymentSerializer(data=requested_data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data
    pay_by = requested_data.get('pay_by').title()
    driver = driver_utils.get_driver(user=request.user)
    if driver:
        reservation = get_object_or_404(Reservation, pk=pk)
        if driver != reservation.driver:
            return Response(lc_utils.failure_response(msg="You are not authorized for this action"))
        if pay_by == 'Cash':
            reservation.reservation_status = Reservation.COMPLETED
            reservation.pay_by = pay_by
            reservation.balance_paid = True
            reservation.save()
            return Response(lc_utils.success_response(msg="Payment made successfully!"))
        if pay_by == 'Credit Card':
            try:
                reservation.client.merchant_account.stripe_id
                try:
                    customer_stripe_id = reservation.client.merchant_account.stripe_id
                    making_payment = merchant_stripe_utils.create_payment_intent(customer_stripe_id,
                                                                                 amount=int(
                                                                                     reservation.balance_fare) * 100,
                                                                                 company=request.user.userprofile.employeeprofilemodel.company)
                    making_payment.confirm(making_payment['id'], payment_method='pm_card_visa', )
                    reservation.reservation_status = Reservation.COMPLETED
                    reservation.pay_by = pay_by
                    reservation.balance_paid = True
                    reservation.save()
                    return Response(lc_utils.success_response(msg="Payment made successfully"))
                except Exception as e:
                    return Response(lc_utils.failure_response(msg="Something Went wrong in transaction"))
            except:
                return Response(lc_utils.failure_response(msg="Payment Method is not Attached"))
    return Response(lc_utils.failure_response(msg="Please login as driver!"))
