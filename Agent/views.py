from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404
from datetime import datetime
from limoucloud_backend import utils as backend_utils
# from Restaurant import models as restaurant_models
from . import tables as agent_table, forms as agent_form, models as agent_models, utils as agent_utils
from Student import models as student_models, forms as student_form
from limoucloud_backend.utils import success_response
from Student import utils as student_utils


# Create your views here.

def all_agents(request):
    agents = agent_models.AgentModel.objects.all()
    sort = request.GET.get('sort', None)
    if sort:
        agents = agents.order_by(sort)
    agents = agent_table.AgentTable(agents)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Commission",
                "href": reverse("add-commission"),
                "icon": "fa fa-plus"
            },
            {
                "color_class": "btn-primary",
                "title": "Add Agent",
                "href": reverse("add-agent"),
                "icon": "fa fa-plus"
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


# ======================+COMMISSION============================================
def add_commission(request):
    today = datetime.today().date()
    if request.method == 'POST':
        form = agent_form.AgentCommissionForm(request.POST)
        student = request.POST.get('student', 0)
        commission_paid = request.POST.get('current_commission_amount', 0)
        if form.is_valid():
            current_commission_amount = request.POST.get('current_commission_amount')
            student_obj = student_models.StudentModel.objects.get(pk=student)
            commission = form.save(commit=False)
            student_obj.total_commission_paid = float(student_obj.total_commission_paid) + float(
                commission_paid) if float(
                student_obj.total_commission_paid) else 0 + float(commission_paid)
            student_obj.previous_commission_history = today
            commission.agent_commission_amount = commission_paid
            student_obj.commission_to_pay = student_obj.commission_to_pay - float(current_commission_amount)
            student_obj.save()
            commission.save()
            messages.success(request, f"Commission Added Successfully!")
            return redirect('all-agent')
        else:
            pass
    else:
        form = agent_form.AgentCommissionForm(initial={'student_paid_fee': 0, 'current_commission_amount': 0})
        context = {
            "page_title": "Add Commission",
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
        ],
        "page_title": f"{agent.name} All Student",
        "table": agent_students,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['student'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


def commission_history(request, pk):
    student_obj = get_object_or_404(student_models.StudentModel, pk=pk)
    agent_obj = get_object_or_404(agent_models.AgentModel, pk=student_obj.agent_name.pk)
    commission_data_history = agent_models.CommissionModelAgent.objects.filter(student=student_obj,
                                                                               agent_name=agent_obj.name,
                                                                               agent_commission_amount__gt=0)
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
        "page_title": f"All Commission From {student_obj.full_name}",
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
    student = request.GET.get('student', '')
    student_obj = student_models.StudentModel.objects.get(pk=student)
    context = {
        'agent': student_obj.agent_name.name,
        'agent_commission_percentage': student_obj.commission,
        'agent_gst': student_obj.gst,
        'agent_commission_amount': student_obj.total_commission_amount,
        'total_commission_paid_till_now': student_obj.total_commission_paid if student_obj.total_commission_paid else 0,
        'commission_to_pay': student_obj.commission_to_pay if student_obj.commission_to_pay else 0,
        'gst_status': student_obj.gst_status if student_obj.gst_status else '',
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
