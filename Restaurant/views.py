from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.generics import get_object_or_404
import datetime
import Menu.models
from limoucloud_backend import utils as backend_utils
from Restaurant import models as restaurant_models
from . import tables as expense_table, forms as expense_form, models as restaurant_models


# Create your views here.


def restaurant_overview(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    restaurant_name = restaurant.name
    contact_first_name = restaurant.user.first_name
    contact_last_name = restaurant.user.last_name
    contact_user_name = restaurant.user.username
    email = restaurant.user.email
    business_phone = restaurant.phone
    address = restaurant.address
    last_paid_date = restaurant.last_paid_date
    active_status = restaurant.active_status
    sales_tax = restaurant.sales_tax

    context = {
        'company_info': 'Company Info',
        'restaurant': restaurant_name,
        'contact_first_Name': contact_first_name,
        'contact_last_name': contact_last_name,
        'contact_user_name': contact_user_name,
        'email': email,
        'business_phone': business_phone,
        'address': address,
        'sales_tax': "{}%".format(sales_tax),
        'last_paid_date': last_paid_date,
        'active_status': active_status,
        'nav_conf': {
            'active_classes': ['restaurant'],
        },
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        # 'button': 'OK'

    }
    return render(request, "company/overview.html", context)


def all_expenses(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    expense = restaurant_models.Expense.objects.filter(restaurant=restaurant)
    sort = request.GET.get('sort', None)
    if sort:
        expense = expense.order_by(sort)
    expense = expense_table.ExpenseTable(expense)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "View Today Expense",
                "href": reverse("restaurant-today-expense"),
                "icon": "fa fa-eye"
            },
            # {
            #     "color_class": "btn-primary",
            #     "title": "Add Expense",
            #     "href": reverse("restaurant-add-expense"),
            #     "icon": "fa fa-plus"
            # },

        ],
        # 'vehicle_count': len(vehicles),
        "page_title": "All Expenses",
        "table": expense,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['expense'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def today_expense(request):
    total_expense = []
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    expense = restaurant_models.Expense.objects.filter(restaurant=restaurant, date=today)
    for exp in expense:
        total_expense.append(exp.price)
    total_expense = sum(total_expense)
    sort = request.GET.get('sort', None)
    if sort:
        expense = expense.order_by(sort)
    expense = expense_table.TodayExpenseTable(expense)
    context = {
        "links": [
            {
                "color_class": "btn-primary",
                "title": "All Expenses",
                "href": reverse("restaurant-all-expenses"),
                "icon": "fa fa-money"
            },
            {
                "color_class": "btn-primary",
                "title": "Add Expense",
                "href": reverse("restaurant-add-expense"),
                "icon": "fa fa-plus"
            },

        ],
        # 'vehicle_count': len(vehicles),
        # "page_title": "All Expenses",
        'total_today_expense': total_expense,
        "table": expense,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'nav_conf': {
            'active_classes': ['expense'],
        },

    }
    return render(request, "dashboard/list-entries.html", context)


def add_expense(request):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    if request.method == "POST":
        form = expense_form.ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.restaurant = restaurant
            expense.save()
            messages.success(request, f"{expense.name} Added Successfully!")
            return redirect("restaurant-all-expenses")
    else:
        form = expense_form.ExpenseForm()
    context = {
        "page_title": "Add expense",
        "form1": form,
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-expenses'),
        'nav_conf': {
            'active_classes': ['vehicles'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def edit_expense(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    expense = get_object_or_404(restaurant_models.Expense, pk=pk, restaurant=restaurant)
    previous_name = expense.name
    if request.method == "POST":
        form = expense_form.ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.save()

            messages.success(request, f" Successfully Updated {previous_name} >> {form.cleaned_data['name']}")
            return redirect('restaurant-all-expenses')
    else:
        form = expense_form.ExpenseForm(instance=expense)
    context = {
        "form1": form,
        "page_title": "Edit Expense",
        "subtitle": "Here you can Edit the Expense",
        "nav_bar": render_to_string("dashboard/company/partials/nav.html"),
        'button': 'Submit',
        'cancel_button': 'Cancel',
        'cancel_button_url': reverse('restaurant-all-expenses'),
        'nav_conf': {
            'active_classes': ['expense'],
        },
    }
    return render(request, "dashboard/add_or_edit.html", context)


def delete_expense(request, pk):
    restaurant: restaurant_models.RestaurantModel = request.user.restaurantmodel
    expense = get_object_or_404(restaurant_models.Expense, pk=pk, restaurant=restaurant)
    backend_utils._delete_table_entry(expense)
    messages.success(request, f"{expense.name} is Deleted Successfully!")
    return redirect('restaurant-all-expenses')
