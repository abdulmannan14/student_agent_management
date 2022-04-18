from django.urls import path
# from Account.views_api import *
from Reservation.api_views import views as reservation_api_views

urlpatterns = [
    path('allreservations', reservation_api_views.AllReservations.as_view(), name='AllReservations'),
    path('service_type', reservation_api_views.ServiceTypes.as_view(), name='service_type'),
    path('vehicle_estimates', reservation_api_views.VehicleEstimates.as_view(), name='vehicle_estimate'),
    path('vehicle_total_fare', reservation_api_views.VehicleTotalFare.as_view(), name='vehicle-total-fare'),
    path('reservations_history', reservation_api_views.ReservationHistory.as_view(), name='reservations-history'),
    path('reservations_conf', reservation_api_views.ReservationConf.as_view(), name='reservations-conf'),
    ]