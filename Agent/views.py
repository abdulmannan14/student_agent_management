from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404
from datetime import datetime
from acmimanagement import utils as backend_utils
# from Restaurant import models as restaurant_models
from . import tables as agent_table, forms as agent_form, models as agent_models, utils as agent_utils
from Student import models as student_models, forms as student_form
from acmimanagement.utils import success_response
from Student import utils as student_utils


# Create your views here.

def all_agents(request):
    agents = agent_models.AgentModel.objects.filter(archived=False)
    sort = request.GET.get('sort', None)
    if sort:
        agents = agents.order_by(sort)
    agents = agent_table.AgentTable(agents)
    context = {
        "links": [

            {
                "color_class": "btn-primary",
                "title": "Add Agent",
                "href": reverse("add-agent"),
                "icon": "fa fa-plus"
            },
            {
                "color_class": "btn-primary",
                "title": "Export Agents",
                "href": reverse("export-agents"),
                "icon": "fa fa-download"
            },
        ],
        # 'vehicle_count': len(vehicles),
        "page_title": "All Agents",
        "table": agents,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['agent'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def add_agent(request):
    if request.method == "POST":
        form = agent_form.AgentForm(request.POST)
        if form.is_valid():
            agent = form.save()
            messages.success(request, f"{agent.name} Added Successfully as Agent!")
            return redirect("all-agent")
    else:
        form = agent_form.AgentForm()
    context = {
        "page_title": "Add agent",
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('all-agent'),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def edit_agent(request, pk):
    agent = get_object_or_404(agent_models.AgentModel, pk=pk)
    if request.method == "POST":
        form = agent_form.AgentForm(request.POST, instance=agent)
        if form.is_valid():
            agent = form.save()
            messages.success(request, f"Agent Updated Successfully")
            return redirect('all-agent')
    else:
        form = agent_form.AgentForm(instance=agent)
    context = {
        "form1": form,
        "page_title": "Edit Agent",
        "subtitle": "Here you can Edit the Agent",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('all-agent'),
        'nav_conf': {
            'active_classes': ['agent'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def delete_agent(request, pk):
    agent = get_object_or_404(agent_models.AgentModel, pk=pk)
    backend_utils._delete_table_entry(agent)
    messages.success(request, f"{agent.name} is Deleted Successfully!")
    return redirect('all-agent')


def archive_agent(request, pk):
    agent_id = pk
    archive_type = request.GET.get('type')

    agent = get_object_or_404(agent_models.AgentModel, pk=pk)
    agent.archived = True
    agent.archived_tag = archive_type
    agent.save()
    messages.success(request, f"{agent.name} is Un-Archived Successfully!")
    return redirect('all-agent')


@login_required(login_url='login')
def archived_agent(request):
    agents = agent_models.AgentModel.objects.filter(archived=True)
    sort = request.GET.get('sort', None)
    if sort:
        agents = agents.order_by(sort)
    agents = agent_table.AgentArchivedTable(agents)
    context = {

        "page_title": "List of Archived Agents",
        "table": agents,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['agent'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


def unarchive_agent(request, pk):
    print("=========entedted")
    agent_id = pk
    archive_type = request.GET.get('type')

    agent = get_object_or_404(agent_models.AgentModel, pk=pk)
    agent.archived = False
    agent.archived_tag = None
    agent.save()
    messages.success(request, f"{agent.name} is Un-Archived Successfully!")
    return redirect('all-agent')


# ======================+COMMISSION============================================
def add_commission(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    today = datetime.today().date()
    if request.method == 'POST':
        course = request.POST.get('student_courses', 0)
        print("this is course=====", course)
        course_obj = student_models.StudentCourse.objects.get(pk=course)
        commission_paid = request.POST.get('total_commission_paid', 0)
        agent_commission_percentage = request.POST.get('agent_commission_percentage')
        agent_commission_amount = request.POST.get('agent_commission_amount')
        current_commission_amount = request.POST.get('current_commission_amount')
        mode_of_payment = request.POST.get('mode_of_payment')
        paid_date = request.POST.get('paid_on')
        comment = request.POST.get('comment')
        agent_models.CommissionModelAgent.objects.create(
            student_course=course_obj,
            agent_name=student.agent_name.name,
            agent_commission_percentage=agent_commission_percentage,
            agent_commission_amount=agent_commission_amount,
            total_commission_paid=commission_paid,
            current_commission_amount=current_commission_amount,
            paid_on=paid_date,
            mode_of_payment=mode_of_payment,
            comment=comment
        )

        course_obj.commission_to_pay = course_obj.commission_to_pay - float(current_commission_amount)
        if not course_obj.total_commission_paid:
            course_obj.total_commission_paid = 0
            course_obj.save()
        course_obj.total_commission_paid = course_obj.total_commission_paid + float(current_commission_amount)
        course_obj.save()
        messages.success(request, f"Commission Added Successfully!")
        return redirect('agent-student-courses', pk)
    else:
        form = agent_form.AgentCommissionForm(initial={'student_paid_fee': 0, 'current_commission_amount': 0})
        print("COURSES=========", student.courses.all())
        form.fields['student_courses'].choices = [('-----', '-----')] + [(course.pk, course) for course in
                                                                         student.courses.all()]

        context = {
            "page_title": f"Add Commission for Student ({student.full_name})",
            "form3": form,
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'button': 'Submit',
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('all-agent'),
            'nav_conf': {
                'active_classes': ['agent'],
            },
            'agent_view': 1,
        }
        return render(request, "dashboard/add_or_edit.html", context)


def edit_commission(request, pk):
    commission_obj = agent_models.CommissionModelAgent.objects.get(pk=pk)
    previous_commission_amount = commission_obj.current_commission_amount
    today = datetime.today().date()
    if request.method == 'POST':
        form = agent_form.AgentCommissionForm(request.POST, instance=commission_obj)
        student = request.POST.get('student', 0)
        # commission_paid = request.POST.get('current_commission_amount', 0)
        if form.is_valid():
            current_commission_amount = request.POST.get('current_commission_amount')
            # calculate_commission_to_add = agent_utils.check_grater_or_lesser(current_commission_amount,
            #                                                                  previous_commission_amount)
            student_obj = student_models.StudentModel.objects.get(pk=student)
            commission = form.save(commit=False)
            student_obj.total_commission_paid = student_obj.total_commission_paid - float(previous_commission_amount)
            student_obj.commission_to_pay = student_obj.commission_to_pay + float(previous_commission_amount)
            student_obj.total_commission_paid = float(student_obj.total_commission_paid) + float(
                current_commission_amount) if float(
                student_obj.total_commission_paid) else 0 + float(current_commission_amount)
            student_obj.previous_commission_history = today
            commission.agent_commission_amount = current_commission_amount
            student_obj.commission_to_pay = student_obj.commission_to_pay - float(current_commission_amount)
            student_obj.save()
            commission.save()
            messages.success(request, f"Commission Edited Successfully!")
            return redirect('commission-history', student)
        else:
            pass
    else:
        form = agent_form.AgentCommissionForm(instance=commission_obj)
        context = {
            "page_title": "Edit Commission",
            "form3": form,
            "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
            'button': 'Submit',
            'cancel_button': 'Cancel',
            'cancel_button_url': reverse('all-agent'),
            'nav_conf': {
                'active_classes': ['agent'],
            },
            'agent_view': 1,
        }
        return render(request, "dashboard/add_or_edit.html", context)


def delete_commission(request, pk):
    print("this is commission object==========================", pk)
    commission_obj = agent_models.CommissionModelAgent.objects.get(pk=pk)
    student_obj = commission_obj.student
    student_obj.total_commission_paid = student_obj.total_commission_paid - float(
        commission_obj.current_commission_amount)
    student_obj.commission_to_pay = student_obj.commission_to_pay + float(commission_obj.current_commission_amount)
    student_obj.save()
    backend_utils._delete_table_entry(commission_obj)
    messages.success(request, f"{commission_obj.agent_name}'s commission Record  is Deleted Successfully!")
    return redirect('all-agent')


def agent_students(request, pk):
    agent = get_object_or_404(agent_models.AgentModel, pk=pk)
    # agent_students = student_models.StudentCourse.objects.filter(studentmodel__agent_name=agent)
    agent_students = student_models.StudentModel.objects.filter(agent_name=agent)
    sort = request.GET.get('sort', None)
    if sort:
        agent_students = agent_students.order_by(sort)
    agent_students = agent_table.AgentStudentTable(agent_students)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "All Agents",
                "href": reverse("all-agent"),
                "icon": "fa fa-graduation-cap"
            },
            # {
            #     "color_class": "btn-primary",
            #     "title": "Export Agent Report",
            #     "href": reverse("export-agent-report", kwargs={'pk': pk}),
            #     "icon": "fa fa-download"
            # },
        ],
        "page_title": f"{agent.name} All Student",
        "table": agent_students,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


def agent_students_courses(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    # agent_students = student_models.StudentCourse.objects.filter(studentmodel__agent_name=agent)
    student_courses = student.courses.all()
    sort = request.GET.get('sort', None)
    if sort:
        student_courses = student_courses.order_by(sort)
    student_courses = agent_table.AgentStudentCourseTable(student_courses)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Commission",
                "href": reverse("add-commission", kwargs={'pk': pk}),
                "icon": "fa fa-plus"
            },
            {
                "color_class": "btn-primary",
                "title": "All Agents",
                "href": reverse("all-agent"),
                "icon": "fa fa-graduation-cap"
            },
            {
                "color_class": "btn-primary",
                "title": "Export Agent Report",
                "href": reverse("export-agent-report", kwargs={'pk': pk}),
                "icon": "fa fa-download"
            },
        ],
        "page_title": f"{student.full_name} All Courses",
        "table": student_courses,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


def commission_history(request, pk):
    print("entered-----")
    student_course = get_object_or_404(student_models.StudentCourse, pk=pk)
    student = student_models.StudentModel.objects.get(courses=student_course)
    commission_data_history = agent_models.CommissionModelAgent.objects.filter(student_course=student_course)
    sort = request.GET.get('sort', None)
    if sort:
        commission_data_history = commission_data_history.order_by(sort)
    commission_data_history = agent_table.AgentCommissionTable(commission_data_history)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "All Agent",
                "href": reverse("all-agent"),
                "icon": "fa fa-graduation-cap"
            },
        ],
        "page_title": f"All Commission From {student.full_name}",
        "table": commission_data_history,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


# ======================================JS WORKING===========================
def get_student_agent_details(request):
    # today = datetime.today()
    student_course = request.GET.get('student_course', '')
    print("this is  student====", student_course)
    student_course_obj = student_models.StudentCourse.objects.get(pk=student_course)
    print("this is student object====", student_course_obj)
    context = {
        # 'agent': student_course_obj.agent_name.name,
        'agent_commission_percentage': student_course_obj.commission,
        'agent_gst': student_course_obj.gst,
        'agent_commission_amount': student_course_obj.total_commission_amount,
        'total_commission_paid_till_now': student_course_obj.total_commission_paid if student_course_obj.total_commission_paid else 0,
        'commission_to_pay': student_course_obj.commission_to_pay if student_course_obj.commission_to_pay else 0,
        'gst_status': student_course_obj.gst_status if student_course_obj.gst_status else '',
    }
    return JsonResponse(success_response(data=context), safe=False)


from datetime import datetime


def send_mail(request, pk):
    commission_obj = student_models.PayModelStudent.objects.get(pk=pk)
    date = commission_obj.paid_on
    date = datetime.strftime(date, "%d-%m-%Y")
    context = {
        'subject': f'Dear Team,',
        'message': f'Hope this email finds you well ! <br>'
                   f' {commission_obj.student.full_name} ({commission_obj.student.acmi_number}) has paid ${commission_obj.fee_pay} on {date}.Kindly send us the invoice at accounts@acmi.wa.edu.au so that we can process the commission accordingly.<br><br>'
                   f'Please note it take 7-10 business days to process the request.<br><br>'
                   f'Regards,<br>'
                   f'Accounts Team <br>'
                   f'ACMi <br><br>'
                   f'Address: Unit 1 / 33 Archer Street, Carlisle Western Australia,Post code: 6101',

        'fee_notice': 'Commission Due Notice'}
    student_utils._thread_making(student_utils.send_email,
                                 ["ACMi Commission Due Notice", context, commission_obj.student.agent_name])
    messages.success(request, "Email sent successfully")
    return redirect('history-student', commission_obj.student.pk)


def export_individual_agent_details(request, pk=None):
    import csv
    from django.http import HttpResponse
    # Create the HttpResponse object with CSV headers.
    student = get_object_or_404(student_models.StudentModel, pk=pk)

    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'] = f'attachment; filename="{student.full_name}_ACMI#{student.acmi_number}_report_for_agent_{student.agent_name.name}.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row (you can modify this according to your table's structure)
    writer.writerow(['Course', 'Start Date', 'End Date', 'Total Fee', 'Total Commission Amount',
                     'Total Commission Paid', 'Commission Yet To Pay'])  # Replace with actual column names

    student_courses = student.courses.all().order_by('-pk').values_list(
        'course__name',
        'start_date', 'end_date',
        'total_fee',
        'total_commission_amount',
        'total_commission_paid',
        'commission_to_pay')
    for row in student_courses:
        writer.writerow(row)

    return response


def export_agents_details(request):
    import csv
    from django.http import HttpResponse
    print("=========+++AJAOoooo============1")
    # Create the HttpResponse object with CSV headers.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="All_Agents.csv"'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row (you can modify this according to your table's structure)
    writer.writerow(['Company', 'Name', 'Email', 'Country', 'Phone', 'Bonus',
                     'Commission To Pay'])  # Replace with actual column names

    agents = agent_models.AgentModel.objects.filter(archived=False).order_by('-pk').values_list(
        'company',
        'name', 'email',
        'country', 'phone',
        'bonus',
    )
    for row in agents:
        student = student_models.StudentModel.objects.filter(agent_name__email=row[2])
        total_commission_to_pay = 0
        for s in student:
            total_commission_to_pay += s.commission_to_pay

        add_total_commission_to_pay = row + (total_commission_to_pay,)
        writer.writerow(add_total_commission_to_pay)

    return response
