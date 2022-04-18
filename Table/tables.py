"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from Order import models as order_models
from . import models as table_models, urls as table_urls
from limoucloud_backend.utils import delete_action
from limoucloud_backend import utils as backend_utils


class TableTable(tables.Table):
    # photo = tables.Column(empty_values=())
    order = tables.Column(empty_values=())
    order_status = tables.Column(empty_values=())
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = table_models.TableModel
        fields = ['table_number', 'table_status', 'order', 'order_status']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            update=table_urls.edit_table(record.pk),
            delete=delete_action(table_urls.delete_table(record.pk), record.table_number),
        )
        )

    def render_order(self, record):
        try:
            order = order_models.OrderModel.objects.filter(table=record).last()
            return order.order_items
        except:
            return None

    def render_order_status(self, record):
        try:
            order = order_models.OrderModel.objects.filter(table=record).last()
            return order.status
        except:
            return None
