from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from Employee import models as employee_model
from Client import models as client_models
from .DoubleEntry.forms import JournalItemForm
from .Vendor import models as vendor_models
from .Transaction.models import Transaction
from Reservation.models import Reservation
from .models import Asset
import datetime
import calendar

from .forms import AssetForm


def income_today(request, company):
    income_today = Transaction.objects.filter(transaction_type='Deposit', dated=datetime.datetime.now(),
                                              company=company).values(
        "dated").order_by('dated').annotate(total_income=Sum('amount'))
    total_income = 0
    for income in income_today:
        total_income += income.get('total_income')

    return total_income


def income_this_month(request, company):
    today = datetime.datetime.now()
    income_this_month = Transaction.objects.filter(transaction_type='Deposit', company=company,
                                                   dated__month=today.month).values(
        "dated").order_by('dated').annotate(total_income=Sum('amount'))
    total_income_this_month = 0
    for income in income_this_month:
        total_income_this_month += income.get('total_income')

    return total_income_this_month


def expense_today(request, company):
    expense_today = Transaction.objects.filter(transaction_type='Withdraw', dated=datetime.datetime.now(),
                                               company=company).values(
        "dated").order_by('dated').annotate(total_expense=Sum('amount'))
    total_expense = 0
    for expense in expense_today:
        total_expense += expense.get('total_expense')

    return total_expense


def expense_this_month(request, company):
    today = datetime.datetime.now()
    expense_this_month = Transaction.objects.filter(transaction_type='Withdraw', company=company,
                                                    dated__month=today.month).values(
        "dated").order_by('dated').annotate(total_expense=Sum('amount'))
    total_expense_this_month = 0
    for expense in expense_this_month:
        total_expense_this_month += expense.get('total_expense')

    return total_expense_this_month


def expense_this_year(request, company, year=None):
    if year is not None:
        today = year
    else:
        today = datetime.datetime.now().year
    expense_this_year = Transaction.objects.filter(transaction_type='Withdraw', company=company,
                                                   dated__year=today).values(
        "dated__month").annotate(total_expense=Sum('amount'))
    income_this_year = Transaction.objects.filter(transaction_type='Deposit', company=company,
                                                  dated__year=today).values(
        "dated__month").annotate(total_income=Sum('amount'))

    income_by_resrevation = Reservation.objects.filter(company=company,
                                                  created_at__year=today).values(
        "created_at__month").annotate(res_income=Sum('base_fare'))


    month_list = get_calender_months()
    expense_list = []
    for month in month_list:
        entry = {
            'month': month.get("number"),
            'expense': 0,
            "income": 0,
            "reservation_income":0,
            'month_name': month.get("name")
        }
        for exp in expense_this_year:
            if month["number"] == exp.get("dated__month"):
                entry["expense"] = exp.get('total_expense')
        for income in income_this_year:
            if month["number"] == income.get("dated__month"):
                entry["income"] = income.get('total_income')
        for income in income_by_resrevation:
            if month["number"] == income.get("created_at__month"):
                entry["reservation_income"] = income.get('res_income')
        expense_list.append(entry)

    return expense_list

def get_calender_months():
    month_list = []
    for month in range(1, 13):
        month_list.append({
            "number": month,
            "name": calendar.month_name[month]
        })
    return month_list
