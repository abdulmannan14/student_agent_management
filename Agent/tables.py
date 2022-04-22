"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from . import models as agent_models, urls as agent_urls
from limoucloud_backend.utils import delete_action
from limoucloud_backend import utils as backend_utils


class AgentTable(tables.Table):
    actions = tables.Column(empty_values=())
    bonus = tables.Column(verbose_name='bonus($)')
    commission = tables.Column(verbose_name='Commission(%)')

    # price = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = agent_models.AgentModel
        fields = ['name', 'email', 'country', 'phone','commission', 'bonus']

    def render_bonus(self, record):
        return "${}".format(record.bonus)

    def render_commission(self, record):
        return "${}".format(record.commission)

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            update=agent_urls.edit_agent(record.pk),
            delete=delete_action(agent_urls.delete_agent(record.pk), record.name),
        )
        )
