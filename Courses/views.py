from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404
from limoucloud_backend import utils as backend_utils
from limoucloud_backend.utils import success_response
from . import models as course_models, tables as course_table, forms as course_form


# Create your views here.


@login_required(login_url='login')
def all_courses(request):
    courses = course_models.Course.objects.all()
    sort = request.GET.get('sort', None)
    if sort:
        courses = courses.order_by(sort)
    courses = course_table.CourseTable(courses)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add course",
                "href": reverse("add-course"),
                "icon": "fa fa-plus"
            },
        ],
        "page_title": "All courses",
        "table": courses,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['course'],
        },
    }
    return render(request, "dashboard/list-entries.html", context)


@login_required(login_url='login')
def add_course(request):
    if request.method == "POST":
        form = course_form.CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            messages.success(request, f"{course.name} Added Successfully as a Course!")
            return redirect("all-course")
    else:
        form = course_form.CourseForm()
    context = {
        "page_title": "Add course",
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('all-course'),
        'nav_conf': {
            'active_classes': ['course'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


@login_required(login_url='login')
def edit_course(request, pk):
    course = get_object_or_404(course_models.Course, pk=pk)
    if request.method == "POST":
        form = course_form.CourseForm(request.POST, instance=course)

        if form.is_valid():
            course = form.save(commit=False)
            course.save()

            messages.success(request, f" course updated Successfully")
            return redirect('all-course')
    else:
        form = course_form.CourseForm(instance=course)
    context = {
        "form1": form,
        "page_title": "Edit course",
        "subtitle": "Here you can Edit the course",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('all-course'),
        'nav_conf': {
            'active_classes': ['course'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def delete_course(request, pk):
    course = get_object_or_404(course_models.Course, pk=pk)
    backend_utils._delete_table_entry(course)
    messages.success(request, f"{course.name} is Deleted Successfully!")
    return redirect('all-course')


def get_course_quarters(request):
    course = course_models.Course.objects.get(pk=request.GET.get('course_id'))
    print("this is course================", course.quarters)
    data = {
        'quarters': course.quarters,
    }
    return JsonResponse(success_response(data=data), safe=False)
