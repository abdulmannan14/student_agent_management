"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from . import models as restaurant_models, urls as restaurant_urls
from limoucloud_backend.utils import delete_action
from limoucloud_backend import utils as backend_utils


class ExpenseTable(tables.Table):
    # actions = tables.Column(empty_values=())
    price = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = restaurant_models.Expense
        fields = ['name', 'price', 'date', 'time']

    # def render_actions(self, record):
    #     return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
    #                        "{delete}".format(
    #         update=restaurant_urls.edit_expense(record.pk),
    #         delete=delete_action(restaurant_urls.delete_expense(record.pk), record.name),
    #     )
    #     )

    def render_price(self, record):
        return "Rs: {}/-".format(record.price)


class TodayExpenseTable(tables.Table):
    actions = tables.Column(empty_values=())
    price = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = restaurant_models.Expense
        fields = ['name', 'price', 'date', 'time']

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            update=restaurant_urls.edit_expense(record.pk),
            delete=delete_action(restaurant_urls.delete_expense(record.pk), record.name),
        )
        )

    def render_price(self, record):
        return "Rs: {}/-".format(record.price)
