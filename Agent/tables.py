"""this file has the tables of vehicles that are using in company and employees views"""
import django_tables2 as tables
from django.utils.html import format_html
from . import models as agent_models, urls as agent_urls
from acmimanagement.utils import delete_action, undo_archive_action, archive_action
from acmimanagement import utils as backend_utils
from Student import models as student_models


class AgentTable(tables.Table):
    actions = tables.Column(empty_values=())
    # bonus = tables.Column(verbose_name='bonus($)')
    commission_to_pay = tables.Column(empty_values=(), verbose_name='Commission To Pay')

    # commission = tables.Column(verbose_name='Commission(%)')

    # price = tables.Column(empty_values=())

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = agent_models.AgentModel
        fields = ['company', 'name', 'email', 'country', 'phone',
                  'commission_to_pay']

    # def render_bonus(self, record):
    #     return "${}".format(record.bonus)

    # def render_commission(self, record):
    #     return "%{}".format(record.commission)

    def render_commission_to_pay(self, record):
        agent_student = student_models.StudentModel.objects.filter(agent_name=record)

        total_commission_to_pay = 0
        for s in agent_student:
            get_all_courses = s.courses.all()
            for course in get_all_courses:
                total_commission_to_pay += course.commission_to_pay
        return "${}".format(total_commission_to_pay)

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-warning' href='{student}'><i class='fa fa-user'></i></a>"
                           "<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
                           "{delete}"
                           "{archive}".format(
            student=agent_urls.agent_students(record.pk),
            update=agent_urls.edit_agent(record.pk),
            delete=delete_action(agent_urls.delete_agent(record.pk), record.name),
            archive=archive_action(agent_urls.archive_agent(record.pk), record.name, modal_name='agentarchiveModal'),
        )
        )


class AgentStudentCourseTable(tables.Table):
    actions = tables.Column(empty_values=())
    # acmi_number = tables.Column(empty_values=(), verbose_name='ACMI Number#')
    course = tables.Column(empty_values=(), verbose_name='Course')
    commission_to_pay = tables.Column(empty_values=(), verbose_name='Commission To Pay')
    total_fee_paid_by_student = tables.Column(empty_values=(), verbose_name='Total Fee Paid By Student')

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = student_models.StudentCourse
        fields = ['course', 'start_date', 'end_date', 'total_fee', 'total_fee_paid_by_student',
                  'total_commission_amount', 'total_commission_paid',
                  'commission_to_pay']

    def render_total_fee_paid_by_student(self, record):
        total_fee_paid = 0
        all_fees = student_models.PayModelStudent.objects.filter(student_course=record,
                                                                 fee_type=student_models.tution_fee)
        for fee in all_fees:
            total_fee_paid += fee.fee_pay
        return "${}".format(total_fee_paid)

    def render_acmi_number(self, record):
        # acmi_numbers = [f"#{student.acmi_number}" for student in record.studentmodel_set.all()]
        return "None"

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


class AgentStudentTable(tables.Table):
    actions = tables.Column(empty_values=())
    acmi_number = tables.Column(empty_values=(), verbose_name='ACMI Number#')

    # course = tables.Column(empty_values=(), verbose_name='Course')
    commission_to_pay = tables.Column(empty_values=(), verbose_name='Commission To Pay')
    total_commission = tables.Column(empty_values=(), verbose_name='Total Commission')
    commission_paid_yet = tables.Column(empty_values=(), verbose_name='Commission Paid Yet')

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = student_models.StudentModel
        fields = ['acmi_number', 'full_name', 'total_commission', 'commission_to_pay', 'commission_paid_yet']

    def render_commission_paid_yet(self, record):
        try:
            student_all_courses = record.courses.all()
            commission_paid_yet = 0
            for course in student_all_courses:
                if course.total_commission_paid:
                    commission_paid_yet += course.total_commission_paid
                else:
                    pass
            return "${}".format(commission_paid_yet)
        except:
            return "${}".format(0)

    def render_total_commission(self, record):
        student_all_courses = record.courses.all()
        total_commission = 0
        for course in student_all_courses:
            total_commission += course.total_commission_amount
        return "${}".format(total_commission)

    def render_commission_to_pay(self, record):
        student_all_courses = record.courses.all()
        commission_to_pay = 0
        for course in student_all_courses:
            commission_to_pay += course.commission_to_pay
        return "${}".format(commission_to_pay)

    def render_acmi_number(self, record):
        # Join them as a comma-separated string (or handle as needed)
        acmi_number = f"#{record.acmi_number}"
        return acmi_number

    def render_actions(self, record):
        return format_html("<a class='btn btn-sm text-warning' href='{history}'><i class='fa fa-book'></i></a>"
        .format(
            history=agent_urls.agentstudentcourses(record.pk),
        )
        )


class AgentCommissionTable(tables.Table):
    # total_commission_paid = tables.Column(empty_values=(), verbose_name='total_commission_paid')
    # actions = tables.Column(empty_values=())
    commission_percentage = tables.Column(empty_values=(), verbose_name='Commission Percentage')
    # current_commission_amount = tables.Column(empty_values=(), verbose_name='Commission to pay')
    current_commission_amount = tables.Column(empty_values=(), verbose_name='Commission Paid')

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = agent_models.CommissionModelAgent
        fields = ['commission_percentage',
                  'current_commission_amount', 'comment',
                  'paid_on', ]

    # def render_current_commission_amount(self, record):
    #     return f"${record.current_commission_amount}"

    def render_commission_percentage(self, record):
        return f"{record.agent_commission_percentage}%"

    def render_current_commission_amount(self, record):
        return "${}".format(record.current_commission_amount)

    # def render_actions(self, record):
    #     return format_html("<a class='btn btn-sm text-primary' href='{update}'><i class='fa fa-pen'></i></a>"
    #                        "{delete}"
    #                        # "<a class='btn btn-sm text-warning' href={send_mail} style=background:#adadad30;><i class='fa fa-envelope' ></i>&nbsp&nbspSend Mail</a>"
    #                        .format(update=agent_urls.edit_agent_commission(record.pk),
    #                                delete=delete_action(agent_urls.delete_agent_commission(record.pk),
    #                                                     record.agent_name),
    #                                # send_mail =agent_urls.send_mail_agent(record.pk)
    #                                )
    #                        )

    # def render_course(self, record):
    #     return "{}".format(record.course)


class AgentArchivedTable(tables.Table):
    actions = tables.Column(empty_values=())
    # acmi_number = tables.Column(verbose_name='ACMI Number#')
    commission_to_pay = tables.Column(empty_values=(), verbose_name='Commission To Pay')
    bonus = tables.Column(verbose_name='bonus($)')

    class Meta:
        attrs = {"class": "table  table-stripped data-table", "data-add-url": "Url here"}
        model = agent_models.AgentModel
        fields = ['company', 'name', 'email', 'country', 'phone', 'bonus',
                  'commission_to_pay']

    def render_actions(self, record):
        return format_html("{unarchive}".format(
            unarchive=undo_archive_action(agent_urls.unarchive_agent(record.pk), record.name),
        )
        )

    def render_bonus(self, record):
        return "${}".format(record.bonus)

        # def render_commission(self, record):
        #     return "%{}".format(record.commission)

    def render_commission_to_pay(self, record):
        student = student_models.StudentModel.objects.filter(agent_name=record)
        total_commission_to_pay = 0
        for s in student:
            total_commission_to_pay += s.commission_to_pay
        return "${}".format(total_commission_to_pay)
