import django_tables2 as tables
from django.utils.html import format_html
from limoucloud_backend.utils import delete_action, detail_action
from . import models as setting_models, urls as setting_urls


class VehicleTypeTable(tables.Table):
    # photo = tables.Column(empty_values=())
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = setting_models.VehicleType
        exclude = ['id', 'company', "image"]

    # def render_photo(self, record):
    #     image_link = "/staticfiles/assets/img/no_image.png"
    #     if record.image:
    #         image_link = record.image.url
    #     return format_html("""
    #     <img height="70px" src='{}'/>
    #     """.format(image_link))

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=setting_urls.edit_vehicle_type(record.pk),
            delete=delete_action(setting_urls.delete_vehicle_type(record.pk), record.all_vehicle_type_name),
            detail=detail_action(setting_urls.detail_vehicle_type(record.pk), record.all_vehicle_type_name)

        )
        )


class ServicetypeTable(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = setting_models.ServiceType
        exclude = ['id', 'company']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=setting_urls.edit_service_type(record.pk),
            delete=delete_action(setting_urls.delete_service_type(record.pk), record.all_service_type_name),
            detail=detail_action(setting_urls.detail_service_type(record.pk), record.all_service_type_name)

        )
        )


class ServicePriceTable(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = setting_models.ServicePrice
        # exclude = ['id','company']
        fields = ("vehicle_type",
                  "service_type",
                  "price_type",
                  "price")

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}".format(
            update=setting_urls.edit_service_price(record.pk),
            # delete=delete_action(setting_urls.delete_service_type(record.pk), record.id),
            detail=detail_action(setting_urls.detail_service_price(record.pk), record.vehicle_type)

        )
        )


class ServiceAreaTable(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = setting_models.ServiceArea
        exclude = ['id', 'company']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=setting_urls.edit_service_area(record.pk),
            delete=delete_action(setting_urls.delete_service_area(record.pk), record.name),
            detail=detail_action(setting_urls.detail_service_area(record.pk), record.name)

        )
        )


class SalesTax(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = setting_models.SalesTax
        exclude = ['id', 'company', 'created_at', 'updated_at']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=setting_urls.edit_sales_tax(record.pk),
            delete=delete_action(setting_urls.delete_sales_tax(record.pk), record.name),
            detail=detail_action(setting_urls.detail_sales_tax(record.pk), record.name)

        )
        )


class ZoneAreaTable(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = setting_models.Zone
        exclude = ['id', 'company']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=setting_urls.edit_zones_area(record.pk),
            delete=delete_action(setting_urls.delete_zones_area(record.pk), record.name),
            detail=detail_action(setting_urls.detail_zones_area(record.pk), record.name)

        )
        )


class AirportsTable(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": 'table table-stripped data-table', 'data-add-url': 'Url here'}
        model = setting_models.CompanyAirport
        exclude = ['id', 'company']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{detail}"
                           "{delete}".format(
            update=setting_urls.edit_airport(record.pk),
            delete=delete_action(setting_urls.delete_airport(record.pk), record),
            detail=detail_action(setting_urls.detail_airport(record.pk), record)

        )
        )
