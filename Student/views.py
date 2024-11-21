from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from datetime import datetime, timedelta

import Courses.models
from acmimanagement import utils as backend_utils
from acmimanagement.utils import success_response
from . import models as student_models, tables as student_table, forms as student_form, utils as student_utils
from Agent import models as agent_models, urls as agent_urls
from django.templatetags.static import static
from datetime import datetime, timedelta, date
from django.contrib.auth.models import User
from . import urls as student_urls
from django.contrib.auth.hashers import check_password
from Courses import urls as course_urls


# import xlwt
# from xlwt import Workbook


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            message = f'Hello {user.username}! You have been logged in'
            messages.success(request, message)
            return redirect('student-index')
        else:
            message = 'Login failed! User Not Found'
            messages.error(request, message)
            return redirect('login')
    else:
        context = {
            'login_page': True,
            # 'header_msg': "ACMi Portal Login",
            # 'header_small_msg': "ACMi Portal Login",
            'logo': True
        }

    return render(request, "dashboard/login.html", context)


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def user_change_password(request):
    user = request.user
    if request.method == 'POST':
        previous_password = request.POST.get('current_password')
        password = request.user.password
        matchcheck = check_password(previous_password, password)
        if not matchcheck:
            messages.error(request, 'Current Password is Incorrect')
            return redirect('change-pass')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')
        if new_password != confirm_new_password:
            messages.error(request, 'New Password and Confirm New Password is not Matching')
            return redirect('change-pass')
        user.set_password(new_password)
        user.save()

        user = authenticate(
            username=user.username,
            password=new_password
        )
        if user is not None:
            login(request, user)

        messages.success(request, 'Password Changed Successfully')

        return redirect('change-pass')
    else:
        context = {
            'change_pass': True,
            "page_title": "Change Password",
            # "form1": form,
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            # 'button': 'Submit',
            # 'cancel_button': 'Cancel',
            # 'cancel_button_url': reverse('all-students'),
            'nav_conf': {
                'active_classes': ['student'],
            },
        }
    return render(request, "dashboard/add_or_edit.html", context)


@csrf_exempt
@login_required(login_url='login')
def index(request):
    today = date.today()
    upcoming_fees = []

    upcoming_fee = student_models.StudentModel.objects.all()
    for i in upcoming_fee:
        upcoming_fees.append(i.outstanding_fee)
    if upcoming_fees:
        try:
            total_upcoming_fee = sum(upcoming_fees)
        except:
            total_upcoming_fee = 0
    else:
        total_upcoming_fee = 0

    commission_to_pay = []
    commissions = student_models.StudentModel.objects.all()
    for i in commissions:
        commission_to_pay.append(i.commission_to_pay)
    total_commissions_to_pay = sum(commission_to_pay)
    total_student = student_models.StudentModel.objects.all()
    total_student = total_student.values('acmi_number').distinct().count()
    total_agents = agent_models.AgentModel.objects.all().count()
    total_enrollments = student_models.StudentModel.objects.all().count()
    total_refunded_student = student_models.StudentModel.objects.filter(refunded=True).count()
    student_report(request)
    context = {
        "cards": [
            # {
            #     "title": "Upcoming Fee",
            #     "value": f"${round(total_upcoming_fee, 2)}",
            #     "icon": "fa-money",
            #     "url": '#'
            #     # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/PendingTrips.svg"),
            # },
            {
                "title": "Fee Collected This Month",
                "value": total_agents,
                "icon": "fa-blind",
                "url": '#'
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            },
            {
                "title": " Commission To Pay",
                "value": f"${round(total_commissions_to_pay, 1)}",
                "icon": "fa-percent",
                "url": '#'
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            },
            {
                "title": "Total Student",
                "value": total_student,
                "icon": "fa-graduation-cap",
                "url": student_urls.all_student()
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/PendingTrips.svg"),
            },
            {
                "title": " Total Agents",
                "value": total_agents,
                "icon": "fa-users",
                "url": agent_urls.all_agent()
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            },
            {
                "title": " Total Enrollments",
                "value": total_enrollments,
                "icon": "fa-book",
                "url": '#'
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            },
            # {
            #     "title": " Total Refunded Student",
            #     "value": total_refunded_student,
            #     "icon": "fa-blind",
            #     "url": reverse('refunded-student')
            #     # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            # },

            {
                "title": "Total Courses",
                "value": Courses.models.Course.objects.all().count(),
                "icon": "fa-blind",
                "url": course_urls.all_course()
                # "icon_path": static("dashboard/assets/img/sidebar/dashboard-card-icons/TripsToday.svg"),
            },

        ],
        'nav_conf': {
            'active_classes': ['index'],
        },
    }
    return render(request, "dashboard/company/index.html", context)


@csrf_exempt
@login_required(login_url='login')
def all_students(request):
    students = student_models.StudentModel.objects.filter(archived=False)
    sort = request.GET.get('sort', None)
    if sort:
        students = students.order_by(sort)
    students = student_table.StudentTable(students)
    context = {
        "links": [
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


@login_required(login_url='login')
def history_student(request, pk):
    # student = get_object_or_404(student_models.StudentModel, pk=pk)
    students = student_models.PayModelStudent.objects.filter(student_course__id=pk)
    student_course = student_models.StudentCourse.objects.filter(id=pk).first()
    student = student_models.StudentModel.objects.filter(courses=student_course).first()
    sort = request.GET.get('sort', None)
    if sort:
        students = students.order_by(sort)
    students = student_table.PayModelStudentTable(students)
    context = {
        "links": [
            # {
            #     "color_class": "btn-primary",
            #     "title": f"Refund {student.full_name}'s Fee",
            #     "icon": "fa fa-undo",
            #     'data_toggle': 'modal',
            #     'data_target': '#refund',
            #     'data_name': f'{student.full_name}',
            # },
            {
                "color_class": "btn-primary",
                "title": "All Student",
                "href": reverse("all-students"),
                "icon": "fa fa-graduation-cap"
            },
        ],
        'redirect_from_modal': student_urls.student_fee_refund(pk),
        "page_title": f"{student.full_name} Payment History for {student_course.course.name}",
        "table": students,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


@login_required(login_url='login')
def student_courses(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    student_courses = student.courses.all()
    print("these are the courses=====", student_courses)
    sort = request.GET.get('sort', None)
    print("these are the Coursses=-=====", student_courses)
    if sort:
        students = student_courses.order_by(sort)
    students = student_table.StudentCoursesTable(student_courses, user_id=student.id)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "All Student",
                "href": reverse("all-students"),
                "icon": "fa fa-graduation-cap"
            },
            {
                "color_class": "btn-primary",
                "title": "Add Fee",
                "href": reverse("add-fee-student", kwargs={"pk": pk}),
                "icon": "fa fa-plus"
            },
            {
                "color_class": "btn-primary",
                "title": "Add Course",
                "href": reverse("add-student-course", kwargs={"pk": pk}),
                "icon": "fa fa-graduation-cap"
            },
        ],
        'redirect_from_modal': student_urls.student_fee_refund(pk),
        "page_title": f"{student.full_name} Courses",
        "table": students,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


def add_student_courses(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    all_courses = Courses.models.Course.objects.all()
    form = student_form.AddCourseForm()
    print("these are the Coursses=-=====11111", all_courses)
    if request.method == "POST":
        course_id = request.POST.get('course')
        course = Courses.models.Course.objects.get(pk=course_id)
        form = student_form.AddCourseForm(request.POST)
        if form.is_valid():
            if student.courses.filter(course=course).exists():
                messages.error(request, f"{student.full_name} Already Enrolled in {course.name}")
                return redirect('student-courses', pk=pk)
            obj = form.save()
            student.courses.add(obj)
            student.save()

        messages.success(request, f"{student.full_name} Added to {course.name} Successfully!")
        return redirect('student-courses', pk=pk)

    # form.fields['name'].queryset = all_courses
    context = {
        "page_title": "Add Student Courses",
        "student": student,
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('student-courses', kwargs={"pk": pk}),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def edit_student_courses(request, pk):
    studentcourse_obj = get_object_or_404(student_models.StudentCourse, pk=pk)
    student = student_models.StudentModel.objects.filter(courses=studentcourse_obj).first()
    if request.method == "POST":
        form = student_form.AddCourseForm(request.POST, instance=studentcourse_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"{studentcourse_obj.course.name} Updated Successfully!")
            return redirect('student-courses', pk=student.id)
    else:
        form = student_form.AddCourseForm(instance=studentcourse_obj)
    context = {
        "page_title": "Edit Student Courses",
        "student": student,
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('student-courses', kwargs={"pk": student.id}),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }

    return render(request, "dashboard/add_or_edit.html", context)


def delete_student_courses(request, pk):
    studentcourse_obj = get_object_or_404(student_models.StudentCourse, pk=pk)
    student = student_models.StudentModel.objects.filter(courses=studentcourse_obj).first()
    studentcourse_obj.delete()
    messages.success(request, f"{studentcourse_obj.course.name} Deleted Successfully!")
    return redirect('student-courses', pk=student.id)


@login_required(login_url='login')
def student_fee_refund(request, pk):
    refund_reason = request.POST.get('refund_reason')
    refunded_way = request.POST.get('refunded_ways')
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    fee_amount = request.POST.get('refund_amount', 0)
    fee_amount = float(fee_amount)
    commission_perc = student.commission
    gst_status = student.gst_status
    gst_perc = student.gst
    commission_amount = 0
    if int(fee_amount) > 0:
        commission_amount = (int(fee_amount) / 100) * commission_perc
        if gst_status == student.COMMISSION_PLUS_GST:
            commission_amount += (commission_amount / 100) * gst_perc
    student: student_models.StudentModel
    student.refunded = True
    student.refund_reason = refund_reason
    student.refund_way = refunded_way
    student.refund_amount = fee_amount
    student.commission_to_pay -= commission_amount
    student.outstanding_fee = 0
    student.save()
    messages.success(request, 'Student Refunded Successfully!')
    return redirect('all-students')


@login_required(login_url='login')
def refunded_student(request):
    students = student_models.StudentModel.objects.filter(refunded=True)
    sort = request.GET.get('sort', None)
    if sort:
        students = students.order_by(sort)
    students = student_table.StudentRefundTable(students)
    context = {

        "page_title": "List of Refunded Student",
        "table": students,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


@login_required(login_url='login')
def archived_student(request):
    students = student_models.StudentModel.objects.filter(archived=True)
    sort = request.GET.get('sort', None)
    if sort:
        students = students.order_by(sort)
    students = student_table.StudentArchivedTable(students)
    context = {

        "page_title": "List of Archived Student",
        "table": students,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


@login_required(login_url='login')
def add_student(request):
    if request.method == "POST":
        form = student_form.StudentForm(request.POST)
        if form.is_valid():
            student_email = form.cleaned_data['email']
            student = student_models.StudentModel.objects.filter(email=student_email)
            if student:
                messages.error(request, f"Student with email {student_email} already exists")
                return redirect("add-student")
            student = form.save(commit=False)
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


#
# @login_required(login_url='login')
# def add_student(request):
#     today = datetime.today()
#     if request.method == "POST":
#         form = student_form.StudentForm(request.POST)
#         if form.is_valid():
#             student_email = form.cleaned_data['email']
#             student = student_models.StudentModel.objects.filter(email=student_email)
#             if student:
#                 messages.error(request, f"Student with email {student_email} already exists")
#                 return redirect("add-student")
#             tuition_fee = form.cleaned_data['tuition_fee']
#             application_fee = form.cleaned_data['application_fee']
#             quarters = form.cleaned_data['course_quarters']
#             quarterly_fee = float(tuition_fee / int(quarters))
#             quarterly_fee = round(quarterly_fee, 2)
#             student = form.save(commit=False)
#             agent_name = form.cleaned_data['agent_name']
#             agent = agent_models.AgentModel.objects.get(company=agent_name)
#             # student.commission = st
#             # student.quarterly_fee_amount = quarterly_fee
#             student.outstanding_fee = quarterly_fee
#             # paid_fee = student.total_fee - student.tuition_fee
#             # student.paid_fee = application_fee
#             student.total_required_fee = student.total_fee
#             student.amount_inserting_date = today.date()
#             student.last_paid_on = today.date()
#
#             student.save()
#             messages.success(request, f"{student.full_name} Added Successfully!")
#             return redirect("all-students")
#     else:
#         form = student_form.StudentForm()
#     context = {
#         "page_title": "Add Student",
#         "form1": form,
#         "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
#         'button': 'Submit',
#         'cancel_button': 'Cancel',
#         'cancel_button_url': reverse('all-students'),
#         'nav_conf': {
#             'active_classes': ['student'],
#         },
#     }
#     return render(request, "dashboard/add_or_edit.html", context)

@login_required(login_url='login')
def edit_student(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    if request.method == "POST":
        form = student_form.StudentForm(request.POST, instance=student)

        if form.is_valid():
            student = form.save(commit=False)
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
    return render(request, "dashboard/add_or_edit.html", context)


# @login_required(login_url='login')
# def edit_student(request, pk):
#     student = get_object_or_404(student_models.StudentModel, pk=pk)
#     if request.method == "POST":
#         form = student_form.StudentForm(request.POST, instance=student)
#
#         if form.is_valid():
#             student = form.save(commit=False)
#             agent_name = form.cleaned_data['agent_name']
#             agent = agent_models.AgentModel.objects.get(company=agent_name)
#             student.commission = form.cleaned_data['commission']
#             student.save()
#
#             messages.success(request, f" Student updated Successfully")
#             return redirect('all-students')
#     else:
#         form = student_form.StudentFormEdit(instance=student)
#     context = {
#         "form1": form,
#         "page_title": "Edit Student",
#         "subtitle": "Here you can Edit the Student",
#         "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
#         'button': 'Submit',
#         'cancel_button': 'Cancel',
#         'cancel_button_url': reverse('all-students'),
#         'nav_conf': {
#             'active_classes': ['student'],
#         },
#     }
#     return render(request, "dashboard/add_or_edit.html", context)
#

def delete_student(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    student_courses = student.courses.all()
    for course in student_courses:
        id = course.id
        obj = student_models.StudentCourse.objects.get(id=id)
        obj.delete()

    backend_utils._delete_table_entry(student)
    messages.success(request, f"{student.full_name} is Deleted Successfully!")
    return redirect('all-students')


def archive_student(request, pk):
    student_id = pk
    archive_type = request.GET.get('type')

    student = get_object_or_404(student_models.StudentModel, pk=pk)
    student.archived = True
    student.archived_tag = archive_type
    student.save()
    messages.success(request, f"{student.full_name} is Un-Archived Successfully!")
    return redirect('all-students')


def unarchive_student(request, pk):
    print("=========entedted")
    student_id = pk
    archive_type = request.GET.get('type')

    student = get_object_or_404(student_models.StudentModel, pk=pk)
    student.archived = False
    student.archived_tag = None
    student.save()
    messages.success(request, f"{student.full_name} is Un-Archived Successfully!")
    return redirect('all-students')


# =====+FEE RELATED+==========================================================
@login_required(login_url='login')
def add_fee(request):
    if request.method == 'POST':
        form = student_form.AddFeeForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            student_obj = student_models.StudentModel.objects.get(pk=student.pk)
            is_oshc_fee = form.cleaned_data['is_oshc_fee']
            is_bonus = form.cleaned_data['is_bonus']
            is_material_fee = form.cleaned_data['is_material_fee']
            is_application_fee = form.cleaned_data['is_application_fee']
            fee_amount = form.cleaned_data['fee_pay']
            paid_on = form.cleaned_data['paid_on']
            if is_bonus:
                form_obj = form.save(commit=False)
                student_obj.is_bonus = True
                form_obj.save()
                student_obj.total_commission_paid += fee_amount
                student_obj.save()
                messages.success(request, "Bonus added successfully")
                return redirect("all-students")
            if is_oshc_fee:
                form_obj = form.save(commit=False)
                student_obj.oshc_fee_paid = True
                form_obj.save()
                messages.success(request, "OSHC Fee added successfully")
                return redirect("all-students")
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
            fee.commission_percentage = student_obj.commission
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


@login_required(login_url='login')
def add_fee_student(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    student_courses = student.courses.all()
    if request.method == 'POST':
        course = request.POST.get('course')
        student_course = student_models.StudentCourse.objects.get(pk=course)
        fee_type = request.POST.get('fee_type')
        fee_amount = request.POST.get('fee_pay')
        paid_on = request.POST.get('paid_on')
        mode_of_payment = request.POST.get('mode_of_payment')
        comment = request.POST.get('comment')

        obj = student_models.PayModelStudent.objects.create(
            student=student,
            student_course=student_course,
            fee_pay=fee_amount,
            paid_on=paid_on,
            fee_type=fee_type,
            agent_commision_amount=(int(student_course.commission) * int(
                fee_amount) / 100) if fee_type == student_models.tution_fee else 0,
            commission_percentage=student_course.commission,
            mode_of_payment=mode_of_payment,
            comment=comment
        )
        # if fee_type == student_models.bonus:
        #     student_obj.is_bonus = True
        #     form_obj.save()
        #     student_obj.total_commission_paid += fee_amount
        #     student_obj.save()
        #     messages.success(request, "Bonus added successfully")
        #     return redirect("all-students")
        # if fee_type == student_models.oshc_fee:
        #     student_course.oshc = fee_amount
        # messages.success(request, "OSHC Fee added successfully")
        # return redirect("all-students")
        # if fee_type == student_models.application_fee:
        #     student_course.application_fee = fee_amount
        # if not student_obj.application_fee_paid:
        #     application_fee_to_subtract = student_obj.application_fee
        #     if student_obj.application_fee <= fee_amount:
        #         fee_amount = fee_amount - application_fee_to_subtract
        #         student_obj.application_fee_paid = True
        # else:
        #     messages.error(request,
        #                    "Process not completed because application fee of this student is already paid")
        #     return redirect("add-fee")
        # if fee_type == student_models.material_fee:
        #     student_course.material_fee = fee_amount
        # if not student_obj.material_fee_paid:
        #     material_fee_to_subtract = student_obj.material_fee
        #     if student_obj.material_fee <= fee_amount:
        #         fee_amount = fee_amount - material_fee_to_subtract
        #         student_obj.material_fee_paid = True
        # else:
        #     messages.error(request,
        #                    "Process not completed because material fee of this student is already paid")
        #     return redirect("add-fee")
        # if fee_amount > 0 and is_material_fee:
        #     if form.cleaned_data['fee_pay'] > student_obj.material_fee:
        #         fee.is_tuition_and_material_fee = True
        if fee_type == student_models.tution_fee:
            calculate_commission_to_pay = student_utils.calculate_commission_including_gst_and_commission(
                student_course,
                fee_amount)
            student_course.commission_to_pay = student_course.commission_to_pay + calculate_commission_to_pay
            student_course.save()
        # fee: student_models.PayModelStudent
        # fee.agent_commision_amount = calculate_commission_to_pay
        # if student_obj.paid_fee >= student_obj.total_fee:
        #     student_obj.outstanding_fee = 0
        # elif student_obj.outstanding_fee == fee_amount:
        #     student_obj.outstanding_fee = 0
        # elif student_obj.outstanding_fee > fee_amount:
        #     student_obj.outstanding_fee = student_obj.outstanding_fee - fee_amount
        # elif fee_amount > student_obj.outstanding_fee:
        #     student_obj.outstanding_fee = 0
        # total_fee_amount = form.cleaned_data['fee_pay']
        # fee.fee_pay = total_fee_amount
        # fee.commission_percentage = student_obj.commission
        # student_obj.total_required_fee = student_obj.total_required_fee - total_fee_amount
        # student_obj.paid_fee = student_obj.paid_fee + total_fee_amount if student_obj.paid_fee else 0 + total_fee_amount
        # # student_obj.material_fee = student_obj.material_fee + fee_amount
        # student_obj.last_paid_on = paid_on
        # student_obj.amount_already_inserted = True
        # student_obj.save()
        # fee.save()
        messages.success(request, f"Fee Added Successfully!")
        return redirect("student-courses", pk=pk)
    else:
        form = student_form.AddFeeForm()
        form.fields['course'].queryset = student_courses
        form1 = student_form.StudentFormAddFee()
        context = {
            "page_title": f" Add Fee ({student.full_name})",
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


@login_required(login_url='login')
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

                    print("this is student outstanding fe=============1", student_obj.outstanding_fee)

                    student_obj.application_fee_paid = False
                    student_obj.material_fee_paid = False

                    deducted_fee_amount = fee_amount
                    deducted_fee_amount = deducted_fee_amount
                    student_obj.outstanding_fee = student_obj.outstanding_fee - deducted_fee_amount

                    print("this is student outstanding fe=============2", student_obj.outstanding_fee)

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

                        #   TODO: Just for Information: Removing Old values from Student Profile.
                        student_obj.paid_fee = student_obj.paid_fee - previous_fee_amount + fee_amount
                        student_obj.outstanding_fee = student_obj.outstanding_fee + deducted_previous_fee_amount
                        print("this is student outstanding fe=============3", student_obj.outstanding_fee)

                        student_obj.application_fee_paid = False

                        if student_obj.material_fee_paid:
                            deducted_fee_amount = fee_amount - student_obj.material_fee
                        else:
                            deducted_fee_amount = fee_amount
                        student_obj.outstanding_fee = student_obj.outstanding_fee - deducted_fee_amount
                        print("this is student outstanding fe=============4", student_obj.outstanding_fee)

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
                        student_obj.material_fee_paid = True
                        if student_obj.application_fee_paid:
                            deducted_fee_amount = fee_amount - student_obj.application_fee
                        else:
                            deducted_fee_amount = fee_amount
                        deducted_fee_amount = deducted_fee_amount - student_obj.material_fee
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
                messages.success(request, f"Fee Edited Successfully!")
                return redirect("all-students")





            # TODO: IF MMATERIAL AND APPLICATION FEE ARE NOT CHANGED
            elif fee.is_application_fee == previous_is_application_fee or fee.is_material_fee == previous_is_material_fee:
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


@login_required(login_url='login')
def delete_fee(request, pk):
    fee_obj = student_models.PayModelStudent.objects.get(pk=pk)
    student_obj = fee_obj.student
    application_fee = 0
    material_fee = 0
    if fee_obj.is_application_fee:
        student_obj.application_fee_paid = False
        application_fee = student_obj.application_fee
    if fee_obj.is_material_fee:
        student_obj.material_fee_paid = False
        material_fee = student_obj.material_fee
    fee_amount = fee_obj.fee_pay
    agent_commission_amount = fee_obj.agent_commision_amount
    student_obj.paid_fee = student_obj.paid_fee - fee_amount
    student_obj.outstanding_fee += (fee_amount - application_fee - material_fee)
    student_obj.commission_to_pay -= agent_commission_amount
    student_obj.save()
    backend_utils._delete_table_entry(fee_obj)
    messages.success(request, f"{student_obj.full_name}'s Fee Record  is Deleted Successfully!")
    return redirect('all-students')


# ======AJAX JAVA SCRIPT======================================================
@login_required(login_url='login')
def get_student_commission(request):
    agent_id = request.GET.get('agent_id', 0)
    agent = get_object_or_404(agent_models.AgentModel, pk=agent_id)
    agent: agent_models.AgentModel
    # agent:agent_models.AgentModel = agent_models.AgentModel.objects.get(pk=agent_id)
    # commission = agent.commission
    data = {
        'commission': agent.commission,
        'gst': 10 if agent.gst_status == agent.COMMISSION_PLUS_GST else 0,
    }
    return JsonResponse(success_response(data=data), safe=False)


from django.db.models import Sum


@login_required(login_url='login')
def get_student_fee_details(request):
    today = datetime.today()
    student_course = request.GET.get('student', '')
    print("this is student", student_course)
    student_course_obj = student_models.StudentCourse.objects.get(pk=student_course)
    # student_obj = student_models.StudentModel.objects.get(courses=student_course_obj)
    # tuition_fee = student_course_obj.tuition_fee
    # outstanding_fee = student_models.PayModelStudent.objects.filter(student_course=student_course_obj,
    #                                                                 paid_on__range=(today - timedelta(days=120), today))

    course_fee_paid_objects = student_models.PayModelStudent.objects.filter(student_course=student_course_obj)
    record_table = []
    for obj in course_fee_paid_objects:
        record_table.append({
            'fee_pay': obj.fee_pay,
            'paid_on': obj.paid_on.strftime('%m-%d-%Y') if obj.paid_on else 'N/A',
            'fee_type': obj.fee_type,
            'mode_of_payment': obj.mode_of_payment,
            'comment': obj.comment if obj.comment else 'N/A'
        })

    total_amount_paid = course_fee_paid_objects.filter(
        student_course_id=student_course_obj.id).aggregate(
        total_paid=Sum('fee_pay')
    )
    context = {
        'total_fee': student_course_obj.total_fee,
        # 'total_required_fee': student_obj.total_required_fee,
        # 'outstanding_fee': student_obj.outstanding_fee,
        # 'already_paid_amount': student_obj.paid_fee if student_obj.paid_fee else 0,
        'already_paid_amount': total_amount_paid['total_paid'],
        'record_table': record_table
    }

    return JsonResponse(success_response(data=context), safe=False)


# ==============STUDENT REPORT===================================
@login_required(login_url='login')
def student_report(request):
    today = datetime.today()
    students = student_models.StudentModel.objects.filter(refunded=False)
    # for student in students:
    #     check_outstanding_fee = student_models.StudentModel.objects.filter(pk=student.id,
    #                                                                        last_paid_on__range=(
    #                                                                            today - timedelta(days=90), today))
    #     if not check_outstanding_fee:
    #         if student.quarterly_fee_amount:
    #             if student.outstanding_fee != student.quarterly_fee_amount and student.outstanding_fee < student.quarterly_fee_amount:
    #                 last_paid_on = student.last_paid_on
    #
    #                 try:
    #                     days_differnece = abs((today.date() - last_paid_on).days)
    #                     amount_inserting_day_difference = abs((today.date() - student.amount_inserting_date).days)
    #                     if days_differnece >= 90:  # and amount_inserting_day_difference >= 90
    #                         student.amount_already_inserted = False
    #
    #                 except:
    #                     pass
    #                 if student.total_required_fee > 0 and student.outstanding_fee == 0:
    #                     student.outstanding_fee = student.quarterly_fee_amount
    #                     student.last_paid_on = today
    #                 elif student.total_required_fee > 0 and student.outstanding_fee > 0 and student.amount_already_inserted is False and student.total_required_fee != student.outstanding_fee:
    #                     student.outstanding_fee = student.quarterly_fee_amount + student.outstanding_fee
    #                     student.amount_already_inserted = True
    #                     student.last_paid_on = today
    #                     student.amount_inserting_date = today.date()
    #                 else:
    #                     student.save()
    #             else:
    #                 last_paid = student.last_paid_on
    #                 days_differnece = abs((today.date() - last_paid).days)
    #                 if days_differnece >= 365:  # and student.amount_already_inserted == False:
    #                     fee_to_add = (4 * student.quarterly_fee_amount) + student.outstanding_fee
    #                     if student.total_required_fee < fee_to_add:
    #                         student.outstanding_fee = student.total_required_fee
    #                         student.last_paid_on = today
    #                     else:
    #                         student.outstanding_fee = fee_to_add
    #                         student.last_paid_on = today
    #                     student.amount_already_inserted = True
    #                     student.amount_inserting_date = today.date()
    #
    #                 elif days_differnece >= 270:  # and student.amount_already_inserted == False:
    #                     fee_to_add = (3 * student.quarterly_fee_amount) + student.outstanding_fee
    #                     if student.total_required_fee < fee_to_add:
    #                         student.outstanding_fee = student.total_required_fee
    #                         student.last_paid_on = today
    #                     else:
    #                         student.outstanding_fee = fee_to_add
    #                         student.last_paid_on = today
    #                     student.amount_already_inserted = True
    #                     student.amount_inserting_date = today.date()
    #                 elif days_differnece >= 180:  # and student.amount_already_inserted == False:
    #                     fee_to_add = (2 * student.quarterly_fee_amount) + student.outstanding_fee
    #                     if student.total_required_fee < fee_to_add:
    #                         student.last_paid_on = today
    #                         student.outstanding_fee = student.total_required_fee
    #                     else:
    #                         student.outstanding_fee = fee_to_add
    #                         student.last_paid_on = today
    #                     student.amount_already_inserted = True
    #                     student.amount_inserting_date = today.date()
    #
    #                 elif days_differnece >= 90:  # and student.amount_already_inserted == False:
    #                     fee_to_add = student.quarterly_fee_amount + student.outstanding_fee
    #                     if student.total_required_fee < fee_to_add:
    #                         student.last_paid_on = today
    #                         student.outstanding_fee = student.total_required_fee
    #                     else:
    #                         student.outstanding_fee = fee_to_add
    #                         student.last_paid_on = today
    #                     student.amount_already_inserted = True
    #                     student.amount_inserting_date = today.date()
    #                 else:
    #                     # student.amount_already_inserted = False
    #                     pass
    #             student.save()
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
        'export_enable': True,

    }
    return render(request, "dashboard/list-entries.html", context)


def send_mail_to_student(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    context = {
        'subject': f'Dear {student.full_name}  ({student.acmi_number}),',
        'message': f' Your $ {student.outstanding_fee} Tuition fee is outstanding; we request you to kindly settle the payment as per agreement so that you can smoothly continue your studies at ACMi.<br><br>'
                   'Regards,<br>'
                   'Accounts Team<br>'
                   'ACMi <br><br>'
                   'RTO Code: 45535 <br>'
                   'CRICOS Code:03800K <br> <br>'
                   'Address: Unit 1 / 33 Archer Street, Carlisle Western Australia,Post code: 6101',
        'fee_notice': 'Student Fee Notice', }
    student_utils._thread_making(student_utils.send_email, ["Welcome to ACMi", context, student])
    student.warning_sent = True
    student.save()
    messages.success(request, "Email sent successfully")
    return redirect('student-report')
