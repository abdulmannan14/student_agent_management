from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from requests import Response
from rest_framework.generics import get_object_or_404
from datetime import datetime, timedelta
from limoucloud_backend import utils as backend_utils
from limoucloud_backend.utils import success_response
from . import models as student_models, tables as student_table, forms as student_form, utils as student_utils
from Agent import models as agent_models
from django.templatetags.static import static
from datetime import datetime, timedelta, date


# Create your views here.

def index(request):
    today = date.today()
    upcoming_fees = []

    upcoming_fee = student_models.StudentModel.objects.all()
    for i in upcoming_fee:
        upcoming_fees.append(i.outstanding_fee)
    total_upcoming_fee = sum(upcoming_fees)

    commission_to_pay = []
    commissions = student_models.StudentModel.objects.all()
    for i in commissions:
        commission_to_pay.append(i.commission_to_pay)
    total_commissions_to_pay = sum(commission_to_pay)
    total_student = student_models.StudentModel.objects.all().count()
    total_agents = agent_models.AgentModel.objects.all().count()

    context = {
        "cards": [
            {
                "title": "Upcoming Fee",
                "value": f"${round(total_upcoming_fee, 2)}",
                "icon": "fa-money",
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/PendingTrips.svg"),
            },
            {
                "title": " Commission To Pay",
                "value": f"${round(total_commissions_to_pay, 1)}",
                "icon": "fa-percent",
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            },
            {
                "title": "Total Student",
                "value": total_student,
                "icon": "fa-graduation-cap",
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/PendingTrips.svg"),
            },
            {
                "title": " Total Agents",
                "value": total_agents,
                "icon": "fa-users",
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            },

        ],
        'driver_trips_info': 'driver_trips_info',
        'vehicles_trips_info': 'vehicles_trips_info',
        'graph_year_data': [5333, 3, 1, 4, 1, 6, 2, 6, 6],
        'get_user_role': 'user_role',
        'nav_conf': {
            'active_classes': ['index'],
        },
    }
    return render(request, "dashboard/company/index.html", context)


def all_students(request):
    students = student_models.StudentModel.objects.all()
    sort = request.GET.get('sort', None)
    if sort:
        students = students.order_by(sort)
    students = student_table.StudentTable(students)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Fee",
                "href": reverse("add-fee"),
                "icon": "fa fa-plus"
            },
            {
                "color_class": "btn-primary",
                "title": "Add Student",
                "href": reverse("add-student"),
                "icon": "fa fa-plus"
            },
        ],
        "page_title": "All Student",
        "table": students,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


def history_student(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    students = student_models.PayModelStudent.objects.filter(student=student, fee_pay__gt=0)
    sort = request.GET.get('sort', None)
    if sort:
        students = students.order_by(sort)
    students = student_table.PayModelStudentTable(students)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "All Student",
                "href": reverse("all-students"),
                "icon": "fa fa-graduation-cap"
            },
        ],
        "page_title": f"{student.full_name} Payment History",
        "table": students,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


def add_student(request):
    today = datetime.today()
    if request.method == "POST":
        form = student_form.StudentForm(request.POST)
        if form.is_valid():
            tuition_fee = form.cleaned_data['tuition_fee']
            application_fee = form.cleaned_data['application_fee']
            quarterly_fee = int(tuition_fee / 4)
            student = form.save(commit=False)
            agent_name = form.cleaned_data['agent_name']
            agent = agent_models.AgentModel.objects.get(company=agent_name)
            student.commission = agent.commission
            student.quarterly_fee_amount = quarterly_fee
            student.outstanding_fee = quarterly_fee
            # paid_fee = student.total_fee - student.tuition_fee
            # student.paid_fee = application_fee
            student.total_required_fee = student.total_fee
            student.amount_inserting_date = today.date()
            student.last_paid_on = today.date()

            student.save()
            messages.success(request, f"{student.full_name} Added Successfully!")
            return redirect("all-students")
    else:
        form = student_form.StudentForm()
    context = {
        "page_title": "Add Student",
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('all-students'),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def edit_student(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    if request.method == "POST":
        form = student_form.StudentForm(request.POST, instance=student)

        if form.is_valid():
            student = form.save(commit=False)
            agent_name = form.cleaned_data['agent_name']
            agent = agent_models.AgentModel.objects.get(company=agent_name)
            student.commission = agent.commission
            student.save()

            messages.success(request, f" Student updated Successfully")
            return redirect('all-students')
    else:
        form = student_form.StudentFormEdit(instance=student)
    context = {
        "form1": form,
        "page_title": "Edit Student",
        "subtitle": "Here you can Edit the Student",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('all-students'),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/edit.html", context)


def delete_student(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    backend_utils._delete_table_entry(student)
    messages.success(request, f"{student.full_name} is Deleted Successfully!")
    return redirect('all-students')


# =====+FEE RELATED+==========================================================
def add_fee(request):
    if request.method == 'POST':
        form = student_form.AddFeeForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            student_obj = student_models.StudentModel.objects.get(pk=student.pk)

            is_material_fee = form.cleaned_data['is_material_fee']
            is_application_fee = form.cleaned_data['is_application_fee']
            fee_amount = form.cleaned_data['fee_pay']
            paid_on = form.cleaned_data['paid_on']
            if is_application_fee:
                if not student_obj.application_fee_paid:
                    application_fee_to_subtract = student_obj.application_fee
                    if student_obj.application_fee <= fee_amount:
                        fee_amount = fee_amount - application_fee_to_subtract
                        student_obj.application_fee_paid = True
                else:
                    messages.error(request,
                                   "Process not completed because application fee of this student is already paid")
                    return redirect("add-fee")
            if is_material_fee:
                if not student_obj.material_fee_paid:
                    material_fee_to_subtract = student_obj.material_fee
                    if student_obj.material_fee <= fee_amount:
                        fee_amount = fee_amount - material_fee_to_subtract
                        student_obj.material_fee_paid = True
                else:
                    messages.error(request,
                                   "Process not completed because material fee of this student is already paid")
                    return redirect("add-fee")
            fee = form.save(commit=False)
            if fee_amount > 0 and is_material_fee:
                if form.cleaned_data['fee_pay'] > student_obj.material_fee:
                    fee.is_tuition_and_material_fee = True
            calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(student_obj,
                                                                                                          fee_amount)
            student_obj.commission_to_pay = student_obj.commission_to_pay + calculate_commission_to_pay
            fee: student_models.PayModelStudent
            fee.agent_commision_amount = calculate_commission_to_pay
            if student_obj.paid_fee >= student_obj.total_fee:
                student_obj.outstanding_fee = 0
            elif student_obj.outstanding_fee == fee_amount:
                student_obj.outstanding_fee = 0
            elif student_obj.outstanding_fee > fee_amount:
                student_obj.outstanding_fee = student_obj.outstanding_fee - fee_amount
            elif fee_amount > student_obj.outstanding_fee:
                student_obj.outstanding_fee = 0
            total_fee_amount = form.cleaned_data['fee_pay']
            fee.fee_pay = total_fee_amount
            student_obj.total_required_fee = student_obj.total_required_fee - total_fee_amount
            student_obj.paid_fee = student_obj.paid_fee + total_fee_amount if student_obj.paid_fee else 0 + total_fee_amount
            # student_obj.material_fee = student_obj.material_fee + fee_amount
            student_obj.last_paid_on = paid_on
            student_obj.amount_already_inserted = True
            student_obj.save()
            fee.save()
            messages.success(request, f"Fee Added Successfully!")
            return redirect("all-students")
        else:
            print("form is not valid$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    else:
        form = student_form.AddFeeForm()
        form1 = student_form.StudentFormAddFee()
        context = {
            "page_title": "Add Fee",
            "form1": form,
            'form2': form1,
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'button': 'Submit',
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('all-students'),
            'nav_conf': {
                'active_classes': ['student'],
            },
        }
        return render(request, "dashboard/add_or_edit.html", context)


def edit_fee(request, pk):
    fee_obj = student_models.PayModelStudent.objects.get(pk=pk)
    previous_fee_amount = fee_obj.fee_pay
    previous_commission_amount = fee_obj.agent_commision_amount
    previous_is_application_fee = fee_obj.is_application_fee
    previous_is_material_fee = fee_obj.is_material_fee
    if request.method == 'POST':
        form = student_form.EditFeeForm(request.POST, instance=fee_obj)
        if form.is_valid():
            student = form.cleaned_data['student']
            paid_on = form.cleaned_data['paid_on']
            fee_amount = form.cleaned_data['fee_pay']
            student_obj = student_models.StudentModel.objects.get(pk=student.pk)
            student_obj: student_models.StudentModel

            fee = form.save(commit=False)
            fee: student_models.PayModelStudent

            # application_fee_of_student = 0
            # fee_amount_to_calculate_commisssion_on = fee_amount
            #
            #   TODO: Just for Information: Checking Previous Is_Application_Fee and Is_Material_Fee.
            if fee.is_application_fee != previous_is_application_fee or fee.is_material_fee != previous_is_material_fee:
                if previous_is_application_fee is False and fee.is_application_fee is True and previous_is_material_fee is False and fee.is_material_fee is True:

                    student_obj.paid_fee = student_obj.paid_fee - previous_fee_amount + fee_amount
                    student_obj.outstanding_fee = student_obj.outstanding_fee + previous_fee_amount

                    student_obj.application_fee_paid = True
                    student_obj.material_fee_paid = True

                    deducted_fee_amount = fee_amount
                    deducted_fee_amount = deducted_fee_amount - student_obj.application_fee - student_obj.material_fee
                    student_obj.outstanding_fee = student_obj.outstanding_fee - deducted_fee_amount

                    if student_obj.paid_fee > student_obj.total_fee:
                        messages.error(request,
                                       f"PROCESS NOT COMPLETED! Student Paid fee is exceeding his Total Fee amount")
                        return redirect("all-students")
                    if student_obj.paid_fee == student_obj.total_fee or deducted_fee_amount == student_obj.outstanding_fee:
                        student_obj.outstanding_fee = 0

                    calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(
                        student_obj, deducted_fee_amount)

                    fee.agent_commision_amount = calculate_commission_to_pay
                    student_obj.commission_to_pay = (student_obj.commission_to_pay - previous_commission_amount) + (
                        calculate_commission_to_pay)
                    student_obj.total_required_fee = student_obj.total_required_fee + previous_fee_amount - fee_amount
                    student_obj.last_paid_on = paid_on
                    student_obj.amount_already_inserted = True
                    student_obj.save()
                    fee.save()
                    student_obj.save()

                    messages.success(request, f"Fee Edited Successfully!")
                    return redirect("all-students")
                if previous_is_application_fee is True and fee.is_application_fee is False and previous_is_material_fee is True and fee.is_material_fee is False:

                    student_obj.paid_fee = student_obj.paid_fee - previous_fee_amount + fee_amount
                    student_obj.outstanding_fee = student_obj.outstanding_fee + (
                            previous_fee_amount - student_obj.application_fee - student_obj.material_fee)
                    print("this is the amount to be addeed=====================",
                          previous_fee_amount - student_obj.application_fee - student_obj.material_fee,
                          'this is overall outstanding fee amount------------------', student_obj.outstanding_fee)
                    student_obj.application_fee_paid = False
                    student_obj.material_fee_paid = False

                    deducted_fee_amount = fee_amount
                    deducted_fee_amount = deducted_fee_amount
                    student_obj.outstanding_fee = student_obj.outstanding_fee - deducted_fee_amount
                    print("this is the amount to be addeed=====================",
                          deducted_fee_amount,
                          'this is overall outstanding fee amount------------------', student_obj.outstanding_fee)

                    if student_obj.paid_fee > student_obj.total_fee:
                        messages.error(request,
                                       f"PROCESS NOT COMPLETED! Student Paid fee is exceeding his Total Fee amount")
                        return redirect("all-students")
                    if student_obj.paid_fee == student_obj.total_fee or deducted_fee_amount == student_obj.outstanding_fee:
                        student_obj.outstanding_fee = 0

                    calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(
                        student_obj, deducted_fee_amount)

                    fee.agent_commision_amount = calculate_commission_to_pay
                    student_obj.commission_to_pay = (student_obj.commission_to_pay - previous_commission_amount) + (
                        calculate_commission_to_pay)
                    student_obj.total_required_fee = student_obj.total_required_fee + previous_fee_amount - fee_amount
                    student_obj.last_paid_on = paid_on
                    student_obj.amount_already_inserted = True
                    student_obj.save()
                    fee.save()
                    student_obj.save()

                    messages.success(request, f"Fee Edited Successfully!")
                    return redirect("all-students")

                if fee.is_application_fee != previous_is_application_fee:
                    if previous_is_application_fee is True and fee.is_application_fee is False:

                        deducted_previous_fee_amount = previous_fee_amount
                        if previous_is_application_fee and previous_is_material_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.material_fee - student_obj.application_fee
                        elif previous_is_application_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.application_fee
                        elif previous_is_material_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.material_fee

                        print("this is previous deduction fee amount==============", deducted_previous_fee_amount)
                        print("this is previous outstanfing fee amount==============", student_obj.outstanding_fee)
                        #   TODO: Just for Information: Removing Old values from Student Profile.
                        student_obj.paid_fee = student_obj.paid_fee - previous_fee_amount + fee_amount
                        student_obj.outstanding_fee = student_obj.outstanding_fee + deducted_previous_fee_amount

                        print("removing=========== paid fee romoving is===", previous_fee_amount,
                              "now st paid feee is ==========", student_obj.paid_fee)
                        print("now st outstanding feee is ==========",
                              student_obj.outstanding_fee)
                        student_obj.application_fee_paid = False

                        if student_obj.material_fee_paid:
                            deducted_fee_amount = fee_amount - student_obj.material_fee
                        else:
                            deducted_fee_amount = fee_amount
                        student_obj.outstanding_fee = student_obj.outstanding_fee - deducted_fee_amount
                        print("removing=========== outstanfing fee romoving is===", deducted_fee_amount,
                              "now st outstanding feee is ==========",
                              student_obj.outstanding_fee)

                        if student_obj.paid_fee > student_obj.total_fee:
                            messages.error(request,
                                           f"PROCESS NOT COMPLETED! Student Paid fee is exceeding his Total Fee amount")
                            return redirect("all-students")
                        if student_obj.paid_fee == student_obj.total_fee or (
                                deducted_fee_amount) == student_obj.outstanding_fee:
                            student_obj.outstanding_fee = 0

                        calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(
                            student_obj, deducted_fee_amount)
                        student_utils._adding_final_values_to_student_and_agent_objects(fee,
                                                                                        calculate_commission_to_pay,
                                                                                        previous_commission_amount,
                                                                                        fee_amount,
                                                                                        student_obj, paid_on,
                                                                                        previous_fee_amount)
                        student_obj.save()
                    elif not previous_is_application_fee and fee.is_application_fee:
                        student_obj.paid_fee = student_obj.paid_fee - previous_fee_amount + fee_amount

                        deducted_previous_fee_amount = previous_fee_amount
                        if previous_is_application_fee and previous_is_material_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.material_fee - student_obj.application_fee
                        elif previous_is_application_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.application_fee
                        elif previous_is_material_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.material_fee

                        student_obj.outstanding_fee = student_obj.outstanding_fee + deducted_previous_fee_amount
                        student_obj.application_fee_paid = True
                        if student_obj.material_fee_paid:
                            deducted_fee_amount = fee_amount - student_obj.material_fee
                        else:
                            deducted_fee_amount = fee_amount
                        deducted_fee_amount = deducted_fee_amount - student_obj.application_fee
                        student_obj.outstanding_fee = student_obj.outstanding_fee - deducted_fee_amount
                        if student_obj.paid_fee > student_obj.total_fee:
                            messages.error(request,
                                           f"PROCESS NOT COMPLETED! Student Paid fee is exceeding his Total Fee amount")
                            return redirect("all-students")
                        if student_obj.paid_fee == student_obj.total_fee or deducted_fee_amount == student_obj.outstanding_fee:
                            student_obj.outstanding_fee = 0

                        calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(
                            student_obj, deducted_fee_amount)

                        fee.agent_commision_amount = calculate_commission_to_pay
                        student_obj.commission_to_pay = (student_obj.commission_to_pay - previous_commission_amount) + (
                            calculate_commission_to_pay)
                        student_obj.total_required_fee = student_obj.total_required_fee + previous_fee_amount - fee_amount
                        student_obj.last_paid_on = paid_on
                        student_obj.amount_already_inserted = True
                        student_obj.save()
                        fee.save()
                        student_obj.save()
                        # messages.success(request, f"Fee Edited Successfully!")
                        # return redirect("all-students")

                if fee.is_material_fee != previous_is_material_fee:
                    if previous_is_material_fee is True and fee.is_material_fee is False:
                        #   TODO: Just for Information: Removing Old values from Student Profile.

                        deducted_previous_fee_amount = previous_fee_amount
                        if previous_is_application_fee and previous_is_material_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.material_fee - student_obj.application_fee
                        elif previous_is_application_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.application_fee
                        elif previous_is_material_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.material_fee

                        student_obj.paid_fee = student_obj.paid_fee - previous_fee_amount + fee_amount
                        student_obj.outstanding_fee = student_obj.outstanding_fee + deducted_previous_fee_amount
                        student_obj.material_fee_paid = False
                        if student_obj.application_fee_paid:
                            deducted_fee_amount = fee_amount - student_obj.application_fee
                        else:
                            deducted_fee_amount = fee_amount
                        student_obj.outstanding_fee = student_obj.outstanding_fee - deducted_fee_amount

                        if student_obj.paid_fee > student_obj.total_fee:
                            messages.error(request,
                                           f"PROCESS NOT COMPLETED! Student Paid fee is exceeding his Total Fee amount")
                            return redirect("all-students")
                        if student_obj.paid_fee == student_obj.total_fee or (
                                deducted_fee_amount) == student_obj.outstanding_fee:
                            student_obj.outstanding_fee = 0

                        calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(
                            student_obj, deducted_fee_amount)
                        student_utils._adding_final_values_to_student_and_agent_objects(fee,
                                                                                        calculate_commission_to_pay,
                                                                                        previous_commission_amount,
                                                                                        fee_amount,
                                                                                        student_obj, paid_on,
                                                                                        previous_fee_amount)
                        student_obj.save()
                        # messages.success(request, f"Fee Edited Successfully!")
                        # return redirect("all-students")
                    elif not previous_is_material_fee and fee.is_material_fee:
                        student_obj.paid_fee = student_obj.paid_fee - previous_fee_amount + fee_amount

                        deducted_previous_fee_amount = previous_fee_amount
                        if previous_is_application_fee and previous_is_material_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.material_fee - student_obj.application_fee
                        elif previous_is_application_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.application_fee
                        elif previous_is_material_fee:
                            deducted_previous_fee_amount = previous_fee_amount - student_obj.material_fee

                        student_obj.outstanding_fee = student_obj.outstanding_fee + deducted_previous_fee_amount
                        print("this is the amount adding in outstandin fee =====", deducted_previous_fee_amount,
                              'thisa isthe new outstanding fee amount====', student_obj.outstanding_fee)
                        student_obj.material_fee_paid = True
                        if student_obj.application_fee_paid:
                            deducted_fee_amount = fee_amount - student_obj.application_fee
                        else:
                            deducted_fee_amount = fee_amount
                        deducted_fee_amount = deducted_fee_amount - student_obj.material_fee
                        student_obj.outstanding_fee = student_obj.outstanding_fee - deducted_fee_amount
                        print("this is the amount adding in outstandin fee ===2==", deducted_fee_amount,
                              'thisa isthe new outstanding fee amount===2=', student_obj.outstanding_fee)
                        if student_obj.paid_fee > student_obj.total_fee:
                            messages.error(request,
                                           f"PROCESS NOT COMPLETED! Student Paid fee is exceeding his Total Fee amount")
                            return redirect("all-students")
                        if student_obj.paid_fee == student_obj.total_fee or (
                                deducted_fee_amount) == student_obj.outstanding_fee:
                            student_obj.outstanding_fee = 0

                        calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(
                            student_obj, deducted_fee_amount)
                        student_utils._adding_final_values_to_student_and_agent_objects(fee,
                                                                                        calculate_commission_to_pay,
                                                                                        previous_commission_amount,
                                                                                        fee_amount,
                                                                                        student_obj, paid_on,
                                                                                        previous_fee_amount)
                        student_obj.save()
                        # messages.success(request, f"Fee Edited Successfully!")
                        # return redirect("all-students")
                messages.success(request, f"Fee Edited Successfully!")
                return redirect("all-students")





            # TODO: IF MMATERIAL AND APPLICATION FEE ARE NOT CHANGED
            elif fee.is_application_fee == previous_is_application_fee or fee.is_material_fee == previous_is_material_fee:
                print("entered=============", fee_amount)
                deducted_fee_amount = fee_amount
                if fee.is_application_fee and fee.is_material_fee:
                    deducted_fee_amount = fee_amount - student_obj.material_fee - student_obj.application_fee
                elif fee.is_application_fee:
                    deducted_fee_amount = fee_amount - student_obj.application_fee
                elif fee.is_material_fee:
                    deducted_fee_amount = fee_amount - student_obj.material_fee

                previous_deducted_fee_amount = previous_fee_amount
                if fee.is_application_fee and fee.is_material_fee:
                    previous_deducted_fee_amount = previous_fee_amount - student_obj.material_fee - student_obj.application_fee
                elif fee.is_application_fee:
                    previous_deducted_fee_amount = previous_fee_amount - student_obj.application_fee
                elif fee.is_material_fee:
                    previous_deducted_fee_amount = previous_fee_amount - student_obj.material_fee
                student_utils._removing_old_values(student_obj, previous_fee_amount, previous_deducted_fee_amount)
                student_utils._adding_new_values(student_obj, fee_amount, deducted_fee_amount)
                student_utils._performing_some_extra_checks(student_obj, request, fee_amount, deducted_fee_amount)
                calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(
                    student_obj, deducted_fee_amount)
                student_utils._adding_final_values_to_student_and_agent_objects(fee, calculate_commission_to_pay,
                                                                                previous_commission_amount, fee_amount,
                                                                                student_obj, paid_on,
                                                                                previous_fee_amount)
            messages.success(request, f"Fee Edited Successfully!")
            return redirect("all-students")
    else:
        form = student_form.EditFeeForm(instance=fee_obj)
        form1 = student_form.StudentFormAddFee(instance=fee_obj.student)
        context = {
            "page_title": "Edit Fee",
            "form1": form,
            'form2': form1,
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'button': 'Submit',
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('all-students'),
            'nav_conf': {
                'active_classes': ['student'],
            },
        }
        return render(request, "dashboard/add_or_edit.html", context)


# ======AJAX JAVA SCRIPT======================================================

def get_agent_commission(request):
    agent_id = request.GET.get('agent_id', 0)
    agent = get_object_or_404(agent_models.AgentModel, pk=agent_id)
    # agent:agent_models.AgentModel = agent_models.AgentModel.objects.get(pk=agent_id)
    commission = agent.commission
    return JsonResponse(success_response(data=commission), safe=False)


def get_student_fee_details(request):
    today = datetime.today()
    student = request.GET.get('student', '')
    student_obj = student_models.StudentModel.objects.get(pk=student)
    tuition_fee = student_obj.tuition_fee
    outstanding_fee = student_models.PayModelStudent.objects.filter(student=student_obj,
                                                                    paid_on__range=(today - timedelta(days=120), today))
    if outstanding_fee:
        context = {
            'total_fee': student_obj.total_fee,
            'total_required_fee': student_obj.total_required_fee,
            'outstanding_fee': student_obj.outstanding_fee,
            'already_paid_amount': student_obj.paid_fee if student_obj.paid_fee else 0,
        }
    else:
        context = {
            'total_fee': student_obj.total_fee,
            'total_required_fee': student_obj.total_required_fee,
            'outstanding_fee': student_obj.outstanding_fee,
            'already_paid_amount': student_obj.paid_fee if student_obj.paid_fee else 0,
        }
    return JsonResponse(success_response(data=context), safe=False)


# ==============STUDENT REPORT===================================

def student_report(request):
    today = datetime.today()
    students = student_models.StudentModel.objects.all()
    for student in students:
        check_outstanding_fee = student_models.StudentModel.objects.filter(pk=student.id,
                                                                           last_paid_on__range=(
                                                                               today - timedelta(days=120), today))
        if not check_outstanding_fee:
            pass
            if student.outstanding_fee != student.quarterly_fee_amount:
                last_paid_on = student.last_paid_on
                try:
                    days_differnece = abs((today.date() - last_paid_on).days)
                    amount_inserting_day_difference = abs((today.date() - student.amount_inserting_date).days)
                    if days_differnece >= 120 and amount_inserting_day_difference >= 120:
                        student.amount_already_inserted = True

                except:
                    pass
                if student.total_required_fee > 0 and student.outstanding_fee == 0:
                    student.outstanding_fee = student.quarterly_fee_amount
                elif student.total_required_fee > 0 and student.outstanding_fee > 0 and student.amount_already_inserted is False and student.total_required_fee != student.outstanding_fee:
                    student.outstanding_fee = student.quarterly_fee_amount + student.outstanding_fee
                    student.amount_already_inserted = True
                    student.amount_inserting_date = today.date()
                else:
                    student.save()
            else:
                last_paid = student.last_paid_on
                days_differnece = abs((today.date() - last_paid).days)
                if days_differnece >= 365:  # and student.amount_already_inserted == False:
                    fee_to_add = (3 * student.quarterly_fee_amount) + student.outstanding_fee
                    if student.total_required_fee < fee_to_add:
                        student.outstanding_fee = student.total_required_fee
                    else:
                        student.outstanding_fee = fee_to_add
                    student.amount_already_inserted = True
                    student.amount_inserting_date = today.date()
                elif days_differnece >= 240:  # and student.amount_already_inserted == False:
                    fee_to_add = (2 * student.quarterly_fee_amount) + student.outstanding_fee
                    if student.total_required_fee < fee_to_add:
                        student.outstanding_fee = student.total_required_fee
                    else:
                        student.outstanding_fee = fee_to_add
                    student.amount_already_inserted = True
                    student.amount_inserting_date = today.date()

                elif days_differnece >= 120:  # and student.amount_already_inserted == False:
                    fee_to_add = student.quarterly_fee_amount + student.outstanding_fee
                    if student.total_required_fee < fee_to_add:
                        student.outstanding_fee = student.total_required_fee
                    else:
                        student.outstanding_fee = fee_to_add
                    student.amount_already_inserted = True
                    student.amount_inserting_date = today.date()
                else:
                    # student.amount_already_inserted = False
                    pass

            student.save()
    sort = request.GET.get('sort', None)
    if sort:
        students = students.order_by(sort)
    students = student_table.StudentTableForReport(students)
    context = {
        "page_title": "Fee Report",
        "table": students,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)
