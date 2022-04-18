import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404

import Order.models
from limoucloud_backend import utils as backend_utils
from Restaurant import models as restaurant_models
from . import tables as order_table, forms as order_form, models as order_models


# Create your views here.
def today_orders(request):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    orders = order_models.OrderModel.objects.filter(restaurant=restaurant, date=today)
    sort = request.GET.get('sort', None)
    if sort:
        orders = orders.order_by(sort)
    order = order_table.OrderTable(orders)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "View All Orders",
                "href": reverse("restaurant-all-orders"),
                "icon": "fa fa-eye"
            },
            {
                "color_class": "btn-primary",
                "title": "Add order",
                "href": reverse("restaurant-add-order"),
                "icon": "fa fa-plus"
            },
        ],
        # 'vehicle_count': len(vehicles),
        "page_title": f"(Today Orders)Total Orders Today : {len(orders)} ",
        "table": order,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['orders'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def all_orders(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    orders = order_models.OrderModel.objects.filter(restaurant=restaurant)
    sort = request.GET.get('sort', None)
    if sort:
        orders = orders.order_by(sort)
    order = order_table.OrderTable(orders)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "Today Orders",
                "href": reverse("restaurant-today-orders"),
                "icon": "fa fa-eye"
            },
        ],
        # 'vehicle_count': len(vehicles),
        "page_title": f"(All Orders) Till Now : {len(orders)} ",
        "table": order,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['orders'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def add_order(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    if request.method == "POST":
        form = order_form.OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.restaurant = restaurant
            order.table.table_status = order.table.OCCUPIED
            order.table.save()
            order.save()
            messages.success(request, f"{order.order_items} Added Successfully for table no {order.table}")
            return redirect("restaurant-all-orders")
    else:
        form = order_form.OrderForm()
    context = {
        "page_title": "Add Order",
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-orders'),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def edit_order(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    order = get_object_or_404(order_models.OrderModel, pk=pk, restaurant=restaurant)
    if request.method == "POST":
        form = order_form.OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()

            messages.success(request, f"Order for Table#{order.table} Is Edited Successfully!")
            return redirect('restaurant-all-orders')
    else:
        form = order_form.OrderForm(instance=order)
    context = {
        "form1": form,
        "page_title": "Edit Order",
        "subtitle": "Here you can Edit the Order",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-orders'),
        'nav_conf': {
            'active_classes': ['order'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def delete_order(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    order = get_object_or_404(order_models.OrderModel, pk=pk, restaurant=restaurant)
    backend_utils._delete_table_entry(order)
    messages.success(request, f"Order with items: {order.order_items} is Deleted Successfully!")
    return redirect('restaurant-all-orders')


def feedback_order(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    orders = order_models.OrderModel.objects.filter(restaurant=restaurant)
    sort = request.GET.get('sort', None)
    if sort:
        orders = orders.order_by(sort)
    order = order_table.OrderFeedbackTable(orders)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "View Today Feedbacks",
                "href": reverse("restaurant-today-feedback"),
                "icon": "fa fa-eye"
            },
        ],
        # 'vehicle_count': len(vehicles),
        "page_title": "All Feedbacks till dated",
        "table": order,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['feedback'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def today_feedback_order(request):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    orders = order_models.OrderModel.objects.filter(restaurant=restaurant, date=today)
    sort = request.GET.get('sort', None)
    if sort:
        orders = orders.order_by(sort)
    order = order_table.OrderFeedbackTable(orders)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "View All Feedbacks",
                "href": reverse("restaurant-feedback-order"),
                "icon": "fa fa-eye"
            },
        ],
        # 'vehicle_count': len(vehicles),
        "page_title": "Today Feedbacks",
        "table": order,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['feedback'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)
