from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404

import Order.models
from limoucloud_backend import utils as backend_utils
from Restaurant import models as restaurant_models
from . import tables as table_table, forms as table_form, models as table_models


# Create your views here.

def all_tables(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    tables = restaurant.tablemodel_set.all()
    sort = request.GET.get('sort', None)
    if sort:
        tables = tables.order_by(sort)
    table = table_table.TableTable(tables)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Table",
                "href": reverse("restaurant-add-table"),
                "icon": "fa fa-plus"
            },
        ],
        # 'vehicle_count': len(vehicles),
        "page_title": "Tables",
        "table": table,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['tables'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def add_table(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    if request.method == "POST":
        form = table_form.TableForm(request.POST, request.FILES)
        if form.is_valid():
            check_table = table_models.TableModel.objects.filter(table_number=form.cleaned_data['table_number'],
                                                                 restaurant=restaurant)
            if not check_table:
                table = form.save(commit=False)
                table.restaurant = restaurant
                table.save()
                messages.success(request, f"{table.table_number} Added Successfully!")
                return redirect("restaurant-all-table")
            else:
                messages.error(request, 'This table number already exists')
                return redirect('restaurant-add-table')
    else:
        form = table_form.TableForm()
    context = {
        "page_title": "Add Fleet",
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-table'),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def edit_table(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    table = get_object_or_404(table_models.TableModel, pk=pk, restaurant=restaurant)
    previous_name = table.table_number
    if request.method == "POST":
        form = table_form.TableForm(request.POST, instance=table)
        if form.is_valid():
            if previous_name == form.cleaned_data['table_number']:
                table = form.save(commit=False)
                table.save()
                messages.success(request,
                                 f" Successfully Updated {previous_name}")
                return redirect('restaurant-all-table')
            else:
                check_table = table_models.TableModel.objects.filter(table_number=form.cleaned_data['table_number'],
                                                                     restaurant=restaurant)
                if not check_table:
                    table = form.save(commit=False)
                    table.save()
                    messages.success(request,
                                     f" Successfully Updated {previous_name} >> {form.cleaned_data['table_number']}")
                    return redirect('restaurant-all-table')
                else:
                    messages.error(request, f'{form.cleaned_data["table_number"]} already exists')
                    return redirect('restaurant-edit-table', pk=pk)

    else:
        form = table_form.TableForm(instance=table)
    context = {
        "form1": form,
        "page_title": "Edit Table",
        "subtitle": "Here you can Edit the Table",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-table'),
        'nav_conf': {
            'active_classes': ['table'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def delete_table(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    table = get_object_or_404(table_models.TableModel, pk=pk, restaurant=restaurant)
    backend_utils._delete_table_entry(table)
    messages.success(request, f"{table.table_number} is Deleted Successfully!")
    return redirect('restaurant-all-table')
