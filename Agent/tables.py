"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from . import models as agent_models, urls as agent_urls
from limoucloud_backend.utils import delete_action
from limoucloud_backend import utils as backend_utils
from Student import models as student_models


class AgentTable(tables.Table):
    actions = tables.Column(empty_values=())
    bonus = tables.Column(verbose_name='bonus($)')
    commission_to_pay = tables.Column(empty_values=(), verbose_name='Commission To Pay')
    commission = tables.Column(verbose_name='Commission(%)')

    # price = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = agent_models.AgentModel
        fields = ['company', 'name', 'email', 'country', 'phone', 'commission', 'bonus', 'commission_to_pay']

    def render_bonus(self, record):
        return "${}".format(record.bonus)

    def render_commission(self, record):
        return "%{}".format(record.commission)

    def render_commission_to_pay(self, record):
        student = student_models.StudentModel.objects.filter(agent_name=record)
        total_commission_to_pay = 0
        for s in student:
            total_commission_to_pay += s.commission_to_pay
        return "${}".format(total_commission_to_pay)

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-warning' href='{student}'><i class='fa fa-user'></i></a>"
                           "<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            student=agent_urls.agent_students(record.pk),
            update=agent_urls.edit_agent(record.pk),
            delete=delete_action(agent_urls.delete_agent(record.pk), record.name),
        )
        )


class AgentStudentTable(tables.Table):
    actions = tables.Column(empty_values=())
    acmi_number = tables.Column(empty_values=(), verbose_name='ACMI Number#')
    course = tables.Column(empty_values=(), verbose_name='Course')
    commission_to_pay = tables.Column(empty_values=(), verbose_name='Commission To Pay')

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = student_models.StudentModel
        fields = ['acmi_number', 'full_name', 'course', 'start_date', 'end_date', 'total_fee',
                  'total_commission_amount', 'total_commission_paid', 'commission_to_pay']

    def render_acmi_number(self, record):
        return "#{}".format(record.acmi_number)

    def render_course(self, record):
        return "{}".format(record.course)

    def render_commission_to_pay(self, record):
        return "${}".format(round(record.commission_to_pay, 1))

    def render_total_commission_paid(self, record):
        return "${}".format(round(record.total_commission_paid, 1))

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-warning' href='{history}'><i class='fa fa-book'></i></a>"
            .format(
            history=agent_urls.commission_history(record.pk),
        )
        )


class AgentCommissionTable(tables.Table):
    # total_commission_paid = tables.Column(empty_values=(), verbose_name='total_commission_paid')
    actions = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = agent_models.CommissionModelAgent
        fields = ['agent_name', 'student', 'student_paid_fee', 'agent_commission_percentage', 'total_commission_paid',
                  'agent_commission_amount', 'paid_on', ]

    def render_total_commission_paid(self, record):
        return "${}".format(record.student.total_commission_paid)

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           .format(update=agent_urls.edit_agent_commission(record.pk))
                           )
    # def render_course(self, record):
    #     return "{}".format(record.course)
