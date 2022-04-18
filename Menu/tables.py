"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from . import models as menu_models, urls as menu_urls
from limoucloud_backend.utils import delete_action
from limoucloud_backend import utils as backend_utils


class MenuHeadTable(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = menu_models.MenuHead
        fields = ['name',]

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            update=menu_urls.edit_menu_head(record.pk),
            delete=delete_action(menu_urls.delete_menu_head(record.pk), record.name),
        )
        )


class MenuItemTable(tables.Table):
    actions = tables.Column(empty_values=())
    price = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = menu_models.MenuItem
        fields = ['name', 'price', 'menu_head']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            update=menu_urls.edit_menu_item(record.pk),
            delete=delete_action(menu_urls.delete_menu_item(record.pk), record.name),
        )
        )

    def render_price(self, record):
        return "Rs: {price}/-".format(price=record.price)
