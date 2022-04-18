"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from Order import models as order_models
from . import models as order_models, urls as order_urls
from limoucloud_backend.utils import delete_action
from limoucloud_backend import utils as backend_utils


class OrderTable(tables.Table):
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = order_models.OrderModel
        fields = ['table', 'order_items', 'status', 'time', 'date', 'bill', 'bill_paid']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            update=order_urls.edit_order(record.pk),
            delete=delete_action(order_urls.delete_order(record.pk), record.order_items),
        )
        )





class OrderFeedbackTable(tables.Table):
    # actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = order_models.OrderModel
        fields = ['table','feedback', 'order_items', 'status', 'time', 'date', 'bill', 'bill_paid']

    # def render_actions(self, record):
    #     return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
    #                        "{delete}".format(
    #         update=order_urls.edit_order(record.pk),
    #         delete=delete_action(order_urls.delete_order(record.pk), record.order_items),
    #     )
    #     )
