"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from . import models as student_models, urls as student_urls
from limoucloud_backend.utils import delete_action
from limoucloud_backend import utils as backend_utils


class PayModelStudentTable(tables.Table):
    status = tables.Column(empty_values=())
    acmi_number = tables.Column(empty_values=(), verbose_name='ACMI Number#')
    course = tables.Column(empty_values=(), verbose_name='Course')

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = student_models.PayModelStudent
        fields = ['acmi_number', 'student', 'course', 'fee_pay', 'paid_on']

    def render_acmi_number(self, record):
        return "#{}".format(record.student.acmi_number)

    def render_course(self, record):
        return "{}".format(record.student.course)

    def render_status(self, record):
        if record.is_material_fee:
            status = "Material Fee"
            bgclass = "bg-blue"
            style = 'border-radius: 5px;'
        else:
            status = "Tuition Fee"
            bgclass = "bg-white"
            style = 'border-radius: 5px;'
        return format_html(
            '<h5 class={bgclass} style={style}>{}</h5>'.format(status, bgclass=bgclass, style=style))


class StudentTable(tables.Table):
    actions = tables.Column(empty_values=())
    acmi_number = tables.Column(verbose_name='ACMI Number#')
    # non_refundable_fee = tables.Column(verbose_name='non refundable fee($)')
    material_fee = tables.Column(verbose_name='material fee($)')
    tuition_fee = tables.Column(verbose_name='tuition fee($)')
    # total_required_fee = tables.Column(verbose_name='total required fee($)')
    # paid_fee = tables.Column(verbose_name='paid fee($)')
    # outstanding_fee = tables.Column(verbose_name='outstanding fee($)')
    # commission = tables.Column(verbose_name='commission(%)')
    discount = tables.Column(verbose_name='discount($)')

    # agent_bonus = tables.Column(verbose_name='agent bonus($)')
    # total_commission_amount = tables.Column(verbose_name='total commission amount($)')

    # previous_commission_history = tables.Column(verbose_name='previous commission history($)')

    # price = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = student_models.StudentModel
        fields = ['acmi_number', 'full_name', 'course', 'phone', 'email', 'total_fee', 'application_fee',
                  'material_fee',
                  'tuition_fee', 'agent_name', 'discount',
                  ]

    def render_acmi_number(self, record):
        return "#{}".format(record.acmi_number)

    # def render_non_refundable_fee(self, record):
    #     return "${}".format(record.non_refundable_fee)

    def render_material_fee(self, record):
        return "${}".format(round(record.material_fee, 2))

    def render_tuition_fee(self, record):
        return "${}".format(round(record.tuition_fee, 2))

    def render_total_required_fee(self, record):
        return "${}".format(round(record.total_required_fee, 2))

    # def render_paid_fee(self, record):
    #     return "${}".format(record.paid_fee)

    # def render_outstanding_fee(self, record):
    #     return "${}".format(record.outstanding_fee)

    # def render_commission(self, record):
    #     return "${}".format(record.commission)

    def render_discount(self, record):
        return "${}".format(round(record.discount, 2))

    # def render_agent_bonus(self, record):
    #     return "${}".format(record.agent_bonus)

    # def render_total_commission_amount(self, record):
    #     return "${}".format(record.total_commission_amount)

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-warning' href='{history}'><i class='fa fa-book'></i></a>"
                           "<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}".format(
            history=student_urls.history_student(record.pk),
            update=student_urls.edit_student(record.pk),
            delete=delete_action(student_urls.delete_student(record.pk), record.full_name),
        )
        )


class StudentTableForReport(tables.Table):
    status = tables.Column(empty_values=())
    acmi_number = tables.Column(verbose_name='ACMI Number#')
    total_required_fee = tables.Column(verbose_name='total required fee($)')
    previous_student_fee_history = tables.Column(empty_values=(), verbose_name='Last Fee Paid History (Y-M-D)')
    # Student Fee History
    outstanding_fee = tables.Column(verbose_name='outstanding fee($)')
    agent_bonus = tables.Column(empty_values=(), verbose_name='agent bonus($)')
    total_commission_amount = tables.Column(verbose_name='Agent Total commission ($)')
    agent_previous_commission_history = tables.Column(empty_values=(), verbose_name='Agent Last Paid on (Y-M-D)')

    # previous_commission_history = tables.Column(verbose_name='previous commission history($)')
    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = student_models.StudentModel
        fields = ['status', 'outstanding_fee', 'acmi_number', 'full_name', 'email', 'course', 'total_fee', 'paid_fee',
                  'total_required_fee',
                  'quarterly_fee_amount', 'previous_student_fee_history', 'agent_name',
                  'total_commission_amount', 'total_commission_paid', 'agent_previous_commission_history',
                  'agent_bonus', 'warning_sent', ]

    def render_acmi_number(self, record):
        return "#{}".format(record.acmi_number)

    def render_previous_student_fee_history(self, record):
        return "Last Paid On : {} ".format(record.last_paid_on)

    def render_agent_previous_commission_history(self, record):
        return "Last Paid On : {}".format(record.previous_commission_history)

    def render_status(self, record):
        if record.total_required_fee < 1:
            status = "Total Paid"
            bgclass = "bg-blue"
            style = 'border-radius: 25px;'
        elif not record.outstanding_fee:
            status = "Clear"
            bgclass = "bg-green"
            style = 'border-radius: 25px;'
        else:
            status = "Not Clear"
            bgclass = "bg-danger"
            style = 'border-radius: 25px;'
        return format_html(
            '<h4 class={bgclass} style={style}>{}</h4>'.format(status, bgclass=bgclass, style=style))

    # def render_non_refundable_fee(self, record):
    #     return "${}".format(record.non_refundable_fee)

    # def render_material_fee(self, record):
    #     return "${}".format(record.material_fee)
    #
    # def render_tuition_fee(self, record):
    #     return "${}".format(record.tuition_fee)

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
        try:
            return "${}".format(record.agent_bonus)
        except:
            return "$ 0"

    def render_total_commission_amount(self, record):
        return "${}".format(record.total_commission_amount)

    # def render_actions(self, record):
    #     return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
    #                        "{delete}".format(
    #         update=student_urls.edit_student(record.pk),
    #         delete=delete_action(student_urls.delete_student(record.pk), record.full_name),
    #     )
    #     )