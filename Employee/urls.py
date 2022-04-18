from django.urls import path, reverse
from . import views as employee_views
from Vehicle import views as vehicle_views
from Client import views as client_views
from Reservation import views as reservation_views

urlpatterns = [
    path("my_profile", employee_views.my_profile, name="my-profile"),
    path("change_password", employee_views.change_pass, name="change-password-employee"),
    path("index_manager", employee_views.index_manager, name="manager-index"),
    path("index_dispatcher", employee_views.index_dispatcher, name="dispatcher-index"),
    # URLS FOR VEHICLES
    path("vehicles/", employee_views.all_vehicle, name="employee-all-vehicle-manager"),
    path("vehicles/add", employee_views.add_vehicle, name="employee-add-vehicle-manager"),
    path("vehicles/<int:pk>/edit", employee_views.edit_vehicle, name="employee-edit-vehicle-manager"),
    path("vehicles/<int:pk>/delete", employee_views.delete_vehicle, name="employee-delete-vehicle-manager"),
    path("vehicles/<int:pk>/details", employee_views.get_vehicle_detail, name="employee-detail-vehicle-manager"),

    # URLS FOR CLIENTS
    path("clients/", employee_views.all_clients, name="employee-all-clients"),
    path("clients/add/general/info", employee_views.add_client_general_info, name="employee-add-client-general-info"),
    path("clients/add/address/info/<str:username>", employee_views.add_client_address_info,
         name="employee-add-client-address-info"),
    path("clients/add/business/info/<str:username>", employee_views.add_client_business_info,
         name="employee-add-client-business-info"),
    path("clients/add/payment/info/<str:username>", employee_views.add_client_payment_info,
         name="employee-add-client-payment-info"),
    path("clients/<int:pk>/edit", employee_views.edit_clients, name="employee-edit-client"),
    path("clients/<int:pk>/delete", employee_views.delete_clients, name="employee-delete-client"),
    path("clients/<int:pk>/details", employee_views.get_client_detail, name="employee-detail-client"),

    # URLS FOR EMPLOYEES
    path("employees", employee_views.all_employee, name="employee-all-employees"),
    path("employees/add", employee_views.add_employee, name="employee-add-employee"),
    path("employees/<int:pk>/edit", employee_views.edit_employee, name="employee-edit-employee"),
    path("employees/<int:pk>/details", employee_views.get_employee_detail, name="employee-detail-employee"),
    path("employees/<int:pk>/delete", employee_views.delete_employee, name="employee-delete-employee"),

    # URLS FOR RESERVATIONS

    path("reservations/", reservation_views.all_reservation, name="employee-all-reservations"),
    path("reservations/add", reservation_views.add_reservation, name="employee-add-reservations"),
    # path("reservations/add/vehicle/<str:vehicle_type>", reservation_views.add_reservation_vehicle,
    #      name="employee-add-reservations-vehicle"),
    path("reservations/<int:pk>/edit", reservation_views.edit_reservation, name="employee-edit-reservations"),
    path("reservations/<int:pk>/delete", reservation_views.delete_reservation, name="employee-delete-reservations")

]


def all_vehicle():
    return reverse("employee-all-vehicle-manager")


def add_vehicle():
    return reverse("employee-add-vehicle-manager")


def edit_vehicle(pk: int):
    return reverse("employee-edit-vehicle-manager", kwargs={"pk": pk})


def delete_vehicle(pk: int):
    return reverse("employee-delete-vehicle-manager", kwargs={"pk": pk})


def get_detail_vehicle(pk: int):
    return reverse('employee-detail-vehicle-manager', kwargs={"pk": pk})


def all_clients():
    return reverse("employee-all-clients")


def add_clients():
    return reverse("employee-add-client-general-info")


def add_clients2(username):
    return reverse("employee-add-client-address-info", kwargs={'username': username})


def add_clients3(username):
    return reverse("employee-add-client-business-info", kwargs={'username': username})


def add_clients4(username):
    return reverse("employee-add-client-payment-info", kwargs={'username': username})


def edit_clients(pk: int):
    return reverse("employee-edit-client", kwargs={"pk": pk})


def delete_clients(pk: int):
    return reverse("employee-delete-client", kwargs={"pk": pk})


def get_detail_client(pk: int):
    return reverse("employee-detail-client", kwargs={'pk': pk})


def index_employee():
    return reverse('employee-index')


def all_employee():
    return reverse("employee-all-employees")


def add_employee():
    return reverse("employee-add-employee")


def edit_employee(pk: int):
    return reverse("employee-edit-employee", kwargs={'pk': pk})


def delete_employee(pk: int):
    return reverse("employee-delete-employee", kwargs={'pk': pk})


def get_detail_employee(pk: int):
    return reverse("employee-detail-employee", kwargs={"pk": pk})


def all_reservation():
    return reverse("employee-all-reservations")


def add_reservation():
    return reverse("employee-add-reservations")


def add_reservation_vehicle(vehicle_type):
    return reverse("employee-add-reservations-vehicle", kwargs={vehicle_type: vehicle_type})


def edit_reservation(pk: int):
    return reverse("employee-edit-reservations", kwargs={'pk': pk})


def all_reservation(pk: int):
    return reverse("employee-delete-reservations", kwargs={'pk': pk})


