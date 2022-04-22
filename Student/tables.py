"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from . import models as student_models, urls as student_urls
from limoucloud_backend.utils import delete_action
from limoucloud_backend import utils as backend_utils


class StudentTable(tables.Table):
    actions = tables.Column(empty_values=())
    acmi_number = tables.Column(verbose_name='ACMI Number#')
    non_refundable_fee = tables.Column(verbose_name='non refundable fee($)')
    material_fee = tables.Column(verbose_name='material fee($)')
    tuition_fee = tables.Column(verbose_name='tuition fee($)')
    total_required_fee = tables.Column(verbose_name='total required fee($)')
    # paid_fee = tables.Column(verbose_name='paid fee($)')
    outstanding_fee = tables.Column(verbose_name='outstanding fee($)')
    # commission = tables.Column(verbose_name='commission(%)')
    discount = tables.Column(verbose_name='discount($)')
    agent_bonus = tables.Column(verbose_name='agent bonus($)')
    total_commission_amount = tables.Column(verbose_name='total commission amount($)')

    # previous_commission_history = tables.Column(verbose_name='previous commission history($)')

    # price = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = student_models.StudentModel
        fields = ['acmi_number', 'full_name', 'non_refundable_fee', 'material_fee', 'tuition_fee', 'total_required_fee',
                  'outstanding_fee', 'previous_student_fee_history', 'agent_name','agent_bonus', 'discount',
                  'total_commission_amount', 'previous_commission_history', 'phone', 'email', 'country']

    def render_acmi_number(self, record):
        return "#{}".format(record.acmi_number)

    def render_non_refundable_fee(self, record):
        return "${}".format(record.non_refundable_fee)

    def render_material_fee(self, record):
        return "${}".format(record.material_fee)

    def render_tuition_fee(self, record):
        return "${}".format(record.tuition_fee)

    def render_total_required_fee(self, record):
        return "${}".format(record.total_required_fee)

    # def render_paid_fee(self, record):
    #     return "${}".format(record.paid_fee)

    def render_outstanding_fee(self, record):
        return "${}".format(record.outstanding_fee)

    # def render_commission(self, record):
    #     return "${}".format(record.commission)

    def render_discount(self, record):
        return "${}".format(record.discount)

    def render_agent_bonus(self, record):
        return "${}".format(record.agent_bonus)

    def render_total_commission_amount(self, record):
        return "${}".format(record.total_commission_amount)

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            update=student_urls.edit_student(record.pk),
            delete=delete_action(student_urls.delete_student(record.pk), record.full_name),
        )
        )
