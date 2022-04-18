from django.urls import path, reverse
from . import views

urlpatterns = [


    path("direct-income", views.direct_income, name="direct-income"),
    path("reservations", views.reservations, name="reservations"),
    path("reservations-payment", views.reservation_payment, name="reservations-payment"),



]
