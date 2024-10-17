from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import StudentModel
from Agent.models import AgentModel
from django.contrib import messages
from . import models as student_models
from acmimanagement.settings import from_email
from threading import Thread


def check_grater_or_lesser(fee_amount, previous_fee_amount):
    if fee_amount != previous_fee_amount:
        new_fee_amount_to_add = fee_amount - previous_fee_amount
    else:
        new_fee_amount_to_add = 0

    return new_fee_amount_to_add


def calculate_gst_if_applicable(commission, student_obj):
    if student_obj.gst_status == student_obj.COMMISSION_PLUS_GST:
        gst_amount = (commission / 100) * student_obj.gst
    else:
        return 0
    return gst_amount


def calculate_commission_including_gst_and_commission(student_obj, fee_amount):
    commission = student_obj.commission * (fee_amount / 100)
    gst = calculate_gst_if_applicable(commission, student_obj)
    new_commission = float(commission) + float(gst)
    return new_commission


def _check_if_now_application_fee_is_false(fee, previous_is_application_fee, student_obj, fee_amount):
    #   TODO: Just for Information: Checking If Application Fee was True Before and False Now
    application_fee_of_student = student_obj.application_fee
    student_obj.application_fee = 0
    student_obj.application_fee_paid = False
    return application_fee_of_student


def calculate_commission_amount_on_fee_amount(student_obj, fee, fee_amount):
    if fee.is_material_fee:
        fee_amount_to_calculate_commisssion_on = fee_amount - student_obj.material_fee
    else:
        fee_amount_to_calculate_commisssion_on = fee_amount
    student_obj.save()
    return fee_amount_to_calculate_commisssion_on


def _check_if_now_application_fee_is_true(request, pk, fee, previous_is_application_fee, student_obj, fee_amount):
    if fee.is_application_fee != previous_is_application_fee:
        #   TODO: Just for Information: Checking If Application Fee was False Before and True Now
        if not previous_is_application_fee and fee.is_application_fee:
            print("entereddddddd=======================================================1 ")
            if not student_obj.application_fee_paid:
                print("entereddddddd=======================================================2")
                application_fee_of_student = student_obj.application_fee
                if student_obj.application_fee <= fee_amount:
                    # fee_amount = fee_amount - application_fee_of_student
                    student_obj.application_fee_paid = True
                    print("entereddddddd=======================================================2 ")
                    if fee.is_material_fee:
                        fee_amount_to_calculate_commisssion_on = fee_amount - student_obj.material_fee
                    else:
                        fee_amount_to_calculate_commisssion_on = fee_amount
                    fee_amount_to_calculate_commisssion_on = fee_amount_to_calculate_commisssion_on - application_fee_of_student
                    application_fee_of_student = -(application_fee_of_student)
                    return True, application_fee_of_student, fee_amount_to_calculate_commisssion_on
                else:
                    return False, "edit-student-fee", pk, "Process not completed because Fee amount is less than Required Application Fee amount"
            else:
                return False, "edit-student-fee", pk, "Process not completed because application fee of this student is already paid"


def _removing_old_values(student_obj, previous_fee_amount, previous_deducted_fee_amount):
    #   TODO: Just for Information: Removing Old values from Student Profile.
    student_obj.paid_fee = student_obj.paid_fee - previous_fee_amount
    student_obj.outstanding_fee = student_obj.outstanding_fee + previous_deducted_fee_amount


def _adding_new_values(student_obj: student_models.StudentModel, fee_amount, deducted_fee_amount):
    student_obj.paid_fee = student_obj.paid_fee + fee_amount
    print("adding=========== paid fee romoving is===", fee_amount, "now st paid feee is ==========",
          student_obj.paid_fee)
    student_obj.outstanding_fee = student_obj.outstanding_fee - deducted_fee_amount
    print("adding=========== outstanfing fee romoving is===", deducted_fee_amount,
          "now st outstanding feee is ==========",
          student_obj.outstanding_fee)


def _performing_some_extra_checks(student_obj, request, fee_amount, deducted_fee_amount):
    if student_obj.paid_fee > student_obj.total_fee:
        messages.success(request, f"PROCESS NOT COMPLETED! Student Paid fee is exceeding his Total Fee amount")
        return redirect("all-students")
    if student_obj.paid_fee == student_obj.total_fee or deducted_fee_amount == student_obj.outstanding_fee:
        student_obj.outstanding_fee = 0


def _adding_final_values_to_student_and_agent_objects(fee, calculate_commission_to_pay, previous_commission_amount,
                                                      fee_amount, student_obj, paid_on, previous_fee_amount):
    fee.agent_commision_amount = calculate_commission_to_pay
    student_obj.commission_to_pay = (student_obj.commission_to_pay - previous_commission_amount) + (
        calculate_commission_to_pay)
    student_obj.total_required_fee = student_obj.total_required_fee + previous_fee_amount - fee_amount
    student_obj.last_paid_on = paid_on
    student_obj.amount_already_inserted = True
    student_obj.save()
    fee.save()


# check_if_now_application_fee_is_false = student_utils._check_if_now_application_fee_is_false(
#                             fee, previous_is_application_fee, student_obj, fee_amount)
#                         application_fee_of_student = check_if_now_application_fee_is_false
#                         fee_amount_to_calculate_commisssion_on = student_utils.calculate_commission_amount_on_fee_amount(
#                             student_obj, fee, fee_amount)
#
#
#                         student_application_fee = student_obj.application_fee
#                         student_material_fee = student_obj.material_fee
#                         print("this is views===============================0",application_fee_of_student)
#                         print("this is views===============================1",student_material_fee)
#                         fee_amount_deducted = fee_amount - student_application_fee - student_material_fee
#                         student_obj.application_fee_paid = False
#                         student_utils._removing_old_values(student_obj, previous_fee_amount)
#                         student_utils._adding_new_values(student_obj, fee_amount_deducted,student_application_fee,student_material_fee)
#                         student_utils._performing_some_extra_checks(student_obj, request, fee_amount)
#                         calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(
#                             student_obj, fee_amount_deducted)
#                         student_utils._adding_final_values_to_student_and_agent_objects(fee,
#                                                                                         calculate_commission_to_pay,
#                                                                                         previous_commission_amount,
#                                                                                         fee_amount, student_obj,
#                                                                                         paid_on, previous_fee_amount)
#


def send_email(subject, context, user=None, email=None, password=None):
    emails = []
    try:
        # emails.append(user.email if user.email else '')
        # emails.append(user.email2 if user.email2 else '')
        # emails.append(user.email3 if user.email3 else '')
        emails.append(user.email)
        emails.append(user.email2)
        emails.append(user.email3)
    except:
        emails.append(user.email)
    html = render_to_string('studentemail.html', context)
    if not subject:
        subject = "Dear {}".format(user.full_name)
    send_mail(
        subject,
        '',
        from_email,
        # recipient_list=['mannanmaan1425@gmail.com'],
        recipient_list=emails,
        html_message=html, fail_silently=False
    )


def _thread_making(target, arguments: list):
    t = Thread(target=target,
               args=arguments)
    t.setDaemon(True)
    t.start()
