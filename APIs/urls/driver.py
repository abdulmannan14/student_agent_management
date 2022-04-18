from django.urls import path
from APIs.views import driver as driver_views

urlpatterns = [
    path("test", driver_views.test),

    path("get-assigned-vehicle", driver_views.get_driver_assigned_vehicle),

    path("reservations", driver_views.get_reservations),
    path("reservations/<int:pk>", driver_views.get_a_reservation),
    path("reservations/<int:pk>/confirm", driver_views.confirm_reservation),
    path("reservations/<int:pk>/update", driver_views.update_reservation),
    path("reservations/<int:pk>/collect-payment", driver_views.collect_reservation_payment),
    path("reservations/new/count", driver_views.get_new_reservation_count),

    path("checklists", driver_views.get_vehicle_checklists),
    path("checklists/options", driver_views.get_vehicle_checklists_options),
    path("checklists/create", driver_views.post_checklist),
    path("checklists/<int:pk>", driver_views.get_a_checklist),
]
