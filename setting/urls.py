from django.urls import path, reverse
from . import views as setting_views

urlpatterns = [
    path('vehicle_type', setting_views.vehicle_type, name='vehicle-type'),
    path('vehicle_type/add', setting_views.add_vehicle_type, name='add-vehicle-type'),
    path('vehicle_type/edit/<int:pk>', setting_views.edit_vehicle_type, name='edit-vehicle-type'),
    path('vehicle_type/delete/<int:pk>', setting_views.delete_vehicle_type, name='delete-vehicle-type'),
    path('vehicle_type/detail/<int:pk>', setting_views.detail_vehicle_type, name='detail-vehicle-type'),
    path('service_type', setting_views.service_type, name='service-types'),
    path('service_type/add', setting_views.add_service_type, name='add-service-types'),
    path('service_type/edit/<int:pk>', setting_views.edit_service_type, name='edit-service-types'),
    path('service_type/delete/<int:pk>', setting_views.delete_service_type, name='delete-service-types'),
    path('service_type/detail/<int:pk>', setting_views.detail_service_type, name='detail-service-types'),
    path('all_pricing', setting_views.all_service_pricing, name='all-service-pricing'),
    # Sales_Tax
    path('sales-tax', setting_views.all_sales_tax, name='all-sales-tax'),
    path('add-sales-tax', setting_views.add_sales_tax, name='add-sales-tax'),
    path('edit-sales-tax/<int:pk>', setting_views.edit_sales_tax, name='edit-sales-tax'),
    path('delete-sales-tax/<int:pk>', setting_views.delete_sales_tax, name='delete-sales-tax'),
    path('view-sales-tax/<int:pk>', setting_views.detail_sales_tax, name='detail-sales-tax'),
    path('sales-tax-amount', setting_views.sales_tax_amount, name='sales-tax-amount'),
    # pricing
    path('all_pricing/edit/<int:pk>/', setting_views.edit_pricing, name='edit-service-pricing'),
    path('all_pricing/detail/<int:pk>/', setting_views.detail_pricing, name='detail-service-pricing'),
    path('all_service_area', setting_views.all_service_area, name='all-service-areas'),

    path('all_service_area/add', setting_views.add_service_area, name='add-service-areas'),

    path('all_service_area/edit/<int:pk>/', setting_views.edit_service_area, name='edit-service-areas'),
    path('all_service_area/delete/<int:pk>/', setting_views.delete_service_area, name='delete-service-areas'),
    path('all_service_area/detail/<int:pk>/', setting_views.detail_service_area, name='detail-service-areas'),
    path('all_zones_area', setting_views.all_zones_area, name='all-zones-areas'),
    path('all_zones_area/add', setting_views.add_zones_area, name='add-zones-areas'),
    path('all_zones_area/edit/<int:pk>/', setting_views.edit_zones_area, name='edit-zones-areas'),
    path('all_zones_area/delete/<int:pk>/', setting_views.delete_zones_area, name='delete-zones-areas'),
    path('all_zones_area/detail/<int:pk>/', setting_views.detail_zones_area, name='detail-zones-areas'),
    #     ===
    path('all_airports', setting_views.all_airport, name='all-airports'),
    path('all_airports/add', setting_views.add_airport, name='add-airports'),
    path('all_airports/edit/<int:pk>/', setting_views.edit_airport, name='edit-airports'),
    path('all_airports/delete/<int:pk>/', setting_views.delete_airport, name='delete-airports'),
    path('all_airports/detail/<int:pk>/', setting_views.detail_airport, name='detail-airports'),
    path('stripe_payment', setting_views.StripePayment, name='stripe-Payment'),
    path('choose_payment', setting_views.Choosepayment, name='choose-payment'),
    path('get_price_basis/', setting_views.get_price_basis, name='get-price-basis'),
    # path('add_zone_price/', setting_views.add_zone_price, name='add-zone-price'),
    path('delete_zone_to_zone/', setting_views.delete_zone_to_zone, name='delete-zone-to-zone'),
    path('get_airport/', setting_views.get_airport, name='get-airport'),
    # company settings
    path('company-settings', setting_views.company_settings, name='company-settings'),
    path('company-settings-account', setting_views.company_settings_account, name='company-settings-account'),
    path('company-settings-billing', setting_views.company_settings_billing, name='company-settings-billing'),
    path('company-settings-change-password', setting_views.company_settings_change_password,
         name='company-settings-change-password'),
    path('company-settings-contact-support', setting_views.company_settings_contact_support,
         name='company-settings-contact-support'),

    # Add new vehicle type
    path('add_new_vehicle_type_company/', setting_views.add_new_vehicle_type_company,
         name='add-new-vehicle-type-company'),
    path('add_new_service_type_company/', setting_views.add_new_service_type_company,
         name='add-new-service-type-company'),
    path('add_new_vehicle_company/', setting_views.add_new_vehicle_company, name='add-new-vehicle-company'),
    path('add_new_position_company/', setting_views.add_new_position_company, name='add-new-position-company'),
    path('package-payment-procees', setting_views.package_payment_proceed, name='package-payment-procees'),

]


def edit_vehicle_type(pk: int):
    return reverse('edit-vehicle-type', kwargs={'pk': pk})


def delete_vehicle_type(pk: int):
    return reverse('delete-vehicle-type', kwargs={'pk': pk})


def detail_vehicle_type(pk: int):
    return reverse('detail-vehicle-type', kwargs={'pk': pk})


def edit_service_type(pk: int):
    return reverse('edit-service-types', kwargs={'pk': pk})


def delete_service_type(pk: int):
    return reverse('delete-service-types', kwargs={'pk': pk})


def detail_service_type(pk: int):
    return reverse('detail-service-types', kwargs={'pk': pk})


def edit_service_price(pk: int):
    return reverse('edit-service-pricing', kwargs={'pk': pk})


def detail_service_price(pk: int):
    return reverse('detail-service-pricing', kwargs={'pk': pk})


def edit_service_area(pk: int):
    return reverse('edit-service-areas', kwargs={'pk': pk})


def delete_service_area(pk: int):
    return reverse('delete-service-areas', kwargs={'pk': pk})


def detail_service_area(pk: int):
    return reverse('detail-service-areas', kwargs={'pk': pk})


# sales_tax


def edit_sales_tax(pk: int):
    return reverse('edit-sales-tax', kwargs={'pk': pk})


def delete_sales_tax(pk: int):
    return reverse('delete-sales-tax', kwargs={'pk': pk})


def detail_sales_tax(pk: int):
    return reverse('detail-sales-tax', kwargs={'pk': pk})


def edit_airport(pk: int):
    return reverse('edit-airports', kwargs={'pk': pk})


def delete_airport(pk: int):
    return reverse('delete-airports', kwargs={'pk': pk})


def detail_airport(pk: int):
    return reverse('detail-airports', kwargs={'pk': pk})


def edit_zones_area(pk: int):
    return reverse('edit-zones-areas', kwargs={'pk': pk})


def delete_zones_area(pk: int):
    return reverse('delete-zones-areas', kwargs={'pk': pk})


def detail_zones_area(pk: int):
    return reverse('detail-zones-areas', kwargs={'pk': pk})
