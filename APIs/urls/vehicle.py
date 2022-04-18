from django.urls import path
from APIs.views import vehicle as vehicle_views

urlpatterns = [
    path("get_all_vehicle/", vehicle_views.get_all_vehicle),
]
