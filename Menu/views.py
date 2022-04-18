from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404

import Menu.models
from limoucloud_backend import utils as backend_utils
from Restaurant import models as restaurant_models
from . import tables as menu_table, forms as menu_form, models as menu_models


# Create your views here.

def all_menu_head(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    menu_head = menu_models.MenuHead.objects.filter(restaurant=restaurant)
    sort = request.GET.get('sort', None)
    if sort:
        menu_head = menu_head.order_by(sort)
    menu_head = menu_table.MenuHeadTable(menu_head)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Menu Head",
                "href": reverse("restaurant-add-menu-head"),
                "icon": "fa fa-plus"
            },
        ],
        # 'vehicle_count': len(vehicles),
        "page_title": "All Menu Head",
        "table": menu_head,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['menu'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def add_menu_head(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    if request.method == "POST":
        form = menu_form.MenuHeadForm(request.POST)
        if form.is_valid():
            menu_head = form.save(commit=False)
            menu_head.restaurant = restaurant
            menu_head.save()
            messages.success(request, f"{menu_head.name} Added Successfully!")
            return redirect("restaurant-all-menu-head")
    else:
        form = menu_form.MenuHeadForm()
    context = {
        "page_title": "Add menu_head",
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-menu-head'),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def edit_menu_head(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    menu_head = get_object_or_404(menu_models.MenuHead, pk=pk, restaurant=restaurant)
    previous_name = menu_head.name
    if request.method == "POST":
        form = menu_form.MenuHeadForm(request.POST, instance=menu_head)

        if form.is_valid():
            menu_head = form.save(commit=False)
            menu_head.save()

            messages.success(request, f" Successfully Updated {previous_name} >> {form.cleaned_data['name']}")
            return redirect('restaurant-all-menu-head')
    else:
        form = menu_form.MenuHeadForm(instance=menu_head)
    context = {
        "form1": form,
        "page_title": "Edit Menu Head",
        "subtitle": "Here you can Edit the Menu Head",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-menu-head'),
        'nav_conf': {
            'active_classes': ['menu_head'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def delete_menu_head(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    menu_head = get_object_or_404(menu_models.MenuHead, pk=pk, restaurant=restaurant)
    backend_utils._delete_table_entry(menu_head)
    messages.success(request, f"{menu_head.name} is Deleted Successfully!")
    return redirect('restaurant-all-menu-head')


# =======================================================================================================================


def all_menu_items(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    menu_item = menu_models.MenuItem.objects.filter(restaurant=restaurant)
    sort = request.GET.get('sort', None)
    if sort:
        menu_item = menu_item.order_by(sort)
    menu_item = menu_table.MenuItemTable(menu_item)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Add Menu Item",
                "href": reverse("restaurant-add-menu-item"),
                "icon": "fa fa-plus"
            },
        ],
        # 'vehicle_count': len(vehicles),
        "page_title": "All Menu Items",
        "table": menu_item,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['menu'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def add_menu_items(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    if request.method == "POST":
        form = menu_form.MenuItemForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            messages.success(request, f"{menu_item.name} Added Successfully in {menu_item.menu_head}")
            return redirect("restaurant-all-menu-item")
    else:
        form = menu_form.MenuItemForm()
    context = {
        "page_title": "Add Menu Item",
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-menu-item'),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def edit_menu_items(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    menu_item = get_object_or_404(menu_models.MenuItem, pk=pk, restaurant=restaurant)
    previous_name = menu_item.name
    if request.method == "POST":
        form = menu_form.MenuItemForm(request.POST, instance=menu_item)

        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.save()

            messages.success(request, f" Successfully Updated {previous_name} >> {form.cleaned_data['name']}")
            return redirect('restaurant-all-menu-item')
    else:
        form = menu_form.MenuItemForm(instance=menu_item)
    context = {
        "form1": form,
        "page_title": "Edit Menu Item",
        "subtitle": "Here you can Edit the Menu Item",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-menu-head'),
        'nav_conf': {
            'active_classes': ['menu_item'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def delete_menu_items(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    row = get_object_or_404(menu_models.MenuHead, pk=pk, restaurant=restaurant)
    backend_utils._delete_table_entry(row)
    messages.success(request, f"{row.name} is Deleted Successfully!")
    return redirect('restaurant-all-menu-head')
