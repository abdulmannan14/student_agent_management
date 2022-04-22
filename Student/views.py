from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from requests import Response
from rest_framework.generics import get_object_or_404
import datetime
import Menu.models
from limoucloud_backend import utils as backend_utils
from limoucloud_backend.utils import success_response
from . import models as student_models, tables as student_table, forms as student_form
from Agent import models as agent_models
from Company import models as compan_models

# Create your views here.

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
                "href": reverse("add-student"),
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


def add_student(request):
    if request.method == "POST":
        form = student_form.StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            agent_name = form.cleaned_data['agent_name']
            agent = agent_models.AgentModel.objects.get(name=agent_name)
            student.commission = agent.commission
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
            'active_classes': ['vehicles'],
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
            agent = agent_models.AgentModel.objects.get(name=agent_name)
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
    return render(request, "dashboard/add_or_edit.html", context)


def delete_student(request, pk):
    student = get_object_or_404(student_models.StudentModel, pk=pk)
    backend_utils._delete_table_entry(student)
    messages.success(request, f"{student.full_name} is Deleted Successfully!")
    return redirect('all-students')


# ============================================================

def get_agent_commission(request):
    agent_id = request.GET.get('agent_id', 0)
    agent = get_object_or_404(agent_models.AgentModel, pk=agent_id)
    agent:agent_models.AgentModel = agent_models.AgentModel.objects.get(pk=agent_id)
    commission = agent.commission
    return JsonResponse(success_response(data=commission), safe=False)
