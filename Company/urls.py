from django.urls import path, reverse, include
from . import views as company_views, utils as company_utils
from Vehicle import views as vehicle_views
from Client import views as client_views
from Employee import views as employee_views
from Reservation import views as reservation_views

urlpatterns = [

    #  URLS FOR COMPANY

    path("edit-profile/", company_views.my_profile, name="my-profile-company"),
    # path("change-password", company_views.change_pass, name="change-password-company"),
    path("index", company_views.index, name="company-index"),
    path("overview", company_views.company_overview, name="company-overview"),
    path("info/update", company_views.update_company_overview, name="company-update"),

    #  URLS FOR EMPLOYEES
    path("employees/", company_views.all_employee, name='company-all-employees'),
    path("employees/add", company_views.add_employee, name='company-add-employee'),
    path("employees/<int:pk>/edit", company_views.edit_employee, name='company-edit-employee'),
    path("employees/<int:pk>/delete", company_views.delete_employee, name='company-delete-employee'),
    path("employees/<int:pk>/detail", company_views.get_employees_detail, name="company-detail-employees"),
    #  URLS FOR VEHICLES
    path("vehicles/", company_views.all_vehicle, name="company-all-vehicles"),
    path("vehicles/add", company_views.add_vehicle, name="company-add-vehicle"),
    path("vehicles/<int:pk>/edit", company_views.edit_vehicle, name="company-edit-vehicle"),
    path("vehicles/<int:pk>/delete", company_views.delete_vehicle, name="company-delete-vehicle"),
    path("vehicle/<int:pk>/detail", company_views.get_vehicle_detail, name="company-detail-vehicle"),

    # URLS FOR CHECKLIST
    path("vehicle/<int:pk>/checklist", company_views.get_vehicle_checklist, name="company-checklist-vehicle"),
    path("vehicle/<int:pk>/checklist/add/", company_views.add_vehicle_checklist, name="company-add-vehicle-checklist"),
    path("vehicles/<int:pk>/checklist/edit/", company_views.edit_checklist, name="company-edit-checklist"),
    path("vehicles/<int:pk>/checklist/delete/", company_views.delete_checklist, name="company-delete-checklist"),
    path("vehicle/<int:pk>/checklist/detail/", company_views.get_checklist_detail, name="company-detail-checklist"),
    #  URLS FOR CLIENTS
    path("clients/", company_views.all_clients, name="company-all-clients"),

    path("clients/add/general/info/<int:client_type>", company_views.add_client,
         name="company-add-client"),
    path("clients/<int:id>/overview", company_views.client_overview, name="client-overview"),
    #
    # path("clients/add/general/info/<str:keyword>/<int:ida>", company_views.add_client_general_info,
    #      name="company-add-client-general-info-reservation"),
    # path("clients/add/address/info/for/<str:username>", company_views.add_client_address_info,
    #      name="company-add-client-address-info"),
    # path("clients/add/address/info/for/<str:username>/<str:keyword>", company_views.add_client_address_info,
    #      name="company-add-client-address-info-reservation"),
    # path("clients/add/business/info/<str:username>", company_views.add_client_business_info,
    #      name="company-add-client-business-info"),
    # path("clients/add/business/info/<str:username>/<str:keyword>", company_views.add_client_business_info,
    #      name="company-add-client-business-info-reservation"),
    # path("clients/add/payment/info/<str:username>", company_views.add_client_payment_info,
    #      name="company-add-client-payment-info"),
    # path("clients/add/payment/info/<str:username>/<str:keyword>", company_views.add_client_payment_info,
    #      name="company-add-client-payment-info-reservation"),
    path("clients/<int:pk>/edit", company_views.edit_clients, name="company-edit-client"),
    path("clients/<int:pk>/delete", company_views.delete_clients, name="company-delete-client"),
    path("clients/<int:pk>/detail", company_views.get_client_detail, name="company-detail-client"),

    # # For Going Back While Creating The Client
    # path("clients/add/general/info/<str:username>/", company_views.back_to_add_client_general_info,
    #      name="company-back-to-add-client-general-info"),
    # path("clients/add/address/info/for/<str:username>/<str:keyword>/", company_views.back_to_add_client_address_info,
    #      name="company-back-to-add-client-address-info"),
    # path("clients/add/business/info/<str:username>/<str:keyword>/", company_views.back_to_add_client_business_info,
    #      name="company-back-to-add-client-business-info"),
    # Employee URLS

    # Reservation URLS

    path("reservations/", reservation_views.all_reservation, name="company-all-reservations"),
    path("reservations/add", reservation_views.add_reservation, name="company-add-reservations"),
    path("get-company-airport", reservation_views.get_company_airport, name="get-company-airport"),
    # path("reservations/add2", reservation_views.add_reservation2, name="company-add-reservations2"),
    # path("reservations/total_charges/<str:total_fare_amount>/", reservation_views.add_reservation_total_charges,
    #      name="company-add-reservations-totalcharges"),
    path('reservation/fare', reservation_views.get_reservation_total_fare, name='get-reservation-fare-amount'),
    path("reservations/<int:pk>/edit", reservation_views.edit_reservation, name="company-edit-reservations"),
    path("reservations/<int:pk>/delete", reservation_views.delete_reservation, name="company-delete-reservations"),
    path("reservations/<int:pk>/detail", reservation_views.detail_reservation, name="company-detail-reservation"),
    path('get_vehicle_type/', reservation_views.get_vehicle_type, name='get-vehicle-type'),
    path('get_airport_latlong/', reservation_views.get_airport_latlong, name='get-airport-latlong'),
    path('get_charge_by_type/', reservation_views.get_charge_type, name='get-charge-by-type'),

    path('get_reservation_price_details/', reservation_views.get_reservation_price_details,
         name='get-reservation-price-details'),
    path('get-distance-in-miles', reservation_views.get_distance_in_miles, name='get-distance-in-miles'),
    # SOME CHECKS URLS
    path('check_email_validity/', company_views.check_email_validity, name='check-email-exist'),

    # COMPANY ALL DISPATCH
    path('dispatches/', company_views.company_dispatches, name='company-all-dispatch'),
    path('dispatch-modify/<int:id>/', company_views.company_dispatch_modify, name='company-modify-dispatch'),

    # Feedback URL
    path('feedback/', company_views.feedback, name='company-feedback'),

    path("clients/<int:pk>/cards/", include("Merchants.urls")),
    # path("clients_tst", company_views.add_client_general_info),
    # Feedback URL
    path('feedback/', company_views.feedback, name='company-feedback'),

    # Dashboard Graph Value
    path('feedback/', company_views.graph_values_generator, name='get-data-acc-to-pressed-btn'),

    # emails
    path('records/', company_views.records, name='company-emails'),
    # help
    path('help/', company_views.help, name='company-help'),
    path('help/get_data', company_views.help_modal_data, name='get_data_for_help_modal'),
    path('client-data', company_utils.get_client_data, name='get-client-details'),

]


def all_vehicle():
    return reverse("company-all-vehicle")


def add_vehicle():
    return reverse("company-add-vehicle")


def edit_vehicle(pk: int):
    return reverse("company-edit-vehicle", kwargs={"pk": pk})


def delete_vehicle(pk: int):
    return reverse("company-delete-vehicle", kwargs={"pk": pk})


def get_detail_vehicle(pk: int):
    return reverse("company-detail-vehicle", kwargs={"pk": pk})


def get_checklist_vehicle(pk: int):
    return reverse("company-checklist-vehicle", kwargs={"pk": pk})


def add_checklist(pk: int):
    return reverse("company-add-vehicle-checklist", kwargs={"pk": pk})


def edit_checklist(pk: int):
    return reverse("company-edit-checklist", kwargs={"pk": pk})


def delete_checklist(pk: int):
    return reverse("company-delete-checklist", kwargs={"pk": pk})


def get_detail_checklist(pk: int):
    return reverse("company-detail-checklist", kwargs={"pk": pk})


def all_clients():
    return reverse("company-all-clients")


def add_clients():
    return reverse("company-add-client")


def add_clients2(username):
    return reverse("company-add-client-address-info", kwargs={'username': username})


def add_clients3(username):
    return reverse("company-add-client-business-info", kwargs={'username': username})


def add_clients4(username):
    return reverse("company-add-client-payment-info", kwargs={'username': username})


def edit_clients(pk: int):
    return reverse("company-edit-client", kwargs={"pk": pk})


def delete_clients(pk: int):
    return reverse("company-delete-client", kwargs={"pk": pk})


def get_detail_client(pk: int):
    return reverse("company-detail-client", kwargs={"pk": pk})


def index_employee():
    return reverse('employee-index')


def all_employee():
    return reverse("company-all-employees")


def add_employee():
    return reverse("company-add-employee")


def edit_employee(pk: int):
    return reverse("company-edit-employee", kwargs={'pk': pk})


def delete_employee(pk: int):
    return reverse("company-delete-employee", kwargs={'pk': pk})


def get_detail_employees(pk: int):
    return reverse("company-detail-employees", kwargs={"pk": pk})


def all_reservation():
    return reverse("company-all-reservations")


def add_reservation():
    return reverse("company-add-reservations")


def add_reservation_vehicle(vehicle_type):
    return reverse("company-add-reservations-vehicle", kwargs={vehicle_type: vehicle_type})


def edit_reservation(pk: int):
    return reverse("company-edit-reservations", kwargs={"pk": pk})


def delete_reservation(pk: int):
    return reverse("company-delete-reservations", kwargs={"pk": pk})


def get_detail_reservation(pk: int):
    return reverse("company-detail-reservation", kwargs={"pk": pk})

# def clients_add_general_info_reservation(key: str, ida):
#     return reverse("company-add-client-general-info-reservation", kwargs={"keyword": key, 'cleint': ida})
