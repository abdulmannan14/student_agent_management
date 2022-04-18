from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from ..DoubleEntry.models import *
from Accounting import utils as accounting_utils

import calendar
import datetime
from django.db.models import Q


# from .models import ChartOfAccount

@login_required
def transactions(request):
    return render(request, "accounting/reports/transaction.html")


@login_required
def account_statement(request):
    company = request.user.userprofile.companyprofilemodel
    journal_items = JournalItem.objects.filter(company=company)
    chart_of_accounts = ChartOfAccount.objects.filter(company=company)
    start_month = request.GET.get('start_month')
    end_month = request.GET.get('end_month')
    account = request.GET.get('account')
    transaction_type = request.GET.get('type')

    if start_month and end_month and account and transaction_type == '':
        date_range = Q(updated_at__range=[start_month, end_month])
        account_type = Q(account=account)
        obj = JournalItem.objects.filter(date_range and account_type)
        account_name = ChartOfAccount.objects.get(id=account).name
        debit_sum = sum([item.debit for item in obj])
        credit_sum = sum([item.credit for item in obj])

        context = {
            'account': account_name,
            'type': 'All',
            'duration': start_month + ' to ' + end_month,
            'journal_items': obj,
            'chart_of_accounts': chart_of_accounts,
            'debit_sum': debit_sum,
            'credit_sum': credit_sum,
            "nav": {
                "parent_active": "reports",
                "child_active": "account_statement", }
        }

        return render(request, "accounting/reports/account_statement.html", context)

    if start_month and end_month and account == '' and transaction_type:
        date_range = Q(updated_at__range=[start_month, end_month])

        if transaction_type == 'Credit':
            obj = JournalItem.objects.filter(date_range, debit=0)
            credit_sum = 0
            for item in obj:
                if item.debit == 0:
                    credit_sum += item.credit
            context = {
                'account': "All",
                'type': transaction_type,
                'duration': start_month + ' to ' + end_month,
                'journal_items': obj,
                'chart_of_accounts': chart_of_accounts,
                'debit_sum': 0,
                'credit_sum': credit_sum,
                "nav": {
                    "parent_active": "reports",
                    "child_active": "account_statement", }
            }
            return render(request, "accounting/reports/account_statement.html", context)

        elif transaction_type == 'Debit':
            obj = JournalItem.objects.filter(date_range, credit=0)
            debit_sum = 0
            for item in obj:
                if item.credit == 0:
                    debit_sum += item.debit

            context = {
                'account': "All",
                'type': transaction_type,
                'duration': start_month + ' to ' + end_month,
                'journal_items': obj,
                'chart_of_accounts': chart_of_accounts,
                'debit_sum': debit_sum,
                'credit_sum': 0,
                "nav": {
                    "parent_active": "reports",
                    "child_active": "account_statement", }
            }
            return render(request, "accounting/reports/account_statement.html", context)

        if start_month and end_month and account == '' and transaction_type:
            date_range = Q(updated_at__range=[start_month, end_month])
            obj = JournalItem.objects.filter(date_range)
            if transaction_type == 'Credit':
                credit_sum = 0
                for item in obj:
                    if item.debit == 0:
                        credit_sum += item.credit
                context = {
                    'account': "All",
                    'type': transaction_type,
                    'duration': start_month + ' to ' + end_month,
                    'journal_items': obj,
                    'chart_of_accounts': chart_of_accounts,
                    'debit_sum': 0,
                    'credit_sum': credit_sum,
                    "nav": {
                        "parent_active": "reports",
                        "child_active": "account_statement", }
                }

                return render(request, "accounting/reports/account_statement.html", context)

            if transaction_type == 'Debit':
                debit_sum = 0
                for item in obj:
                    if item.credit == 0:
                        debit_sum += item.debit
                context = {
                    'account': "All",
                    'type': transaction_type,
                    'duration': start_month + ' to ' + end_month,
                    'journal_items': obj,
                    'chart_of_accounts': chart_of_accounts,
                    'debit_sum': debit_sum,
                    'credit_sum': 0,
                    "nav": {
                        "parent_active": "reports",
                        "child_active": "account_statement", }
                }

                return render(request, "accounting/reports/account_statement.html", context)

    if start_month and end_month and account and transaction_type:
        date_range = Q(updated_at__range=[start_month, end_month])
        account_type = Q(account=account)
        obj = JournalItem.objects.filter(date_range and account_type)
        account_name = ChartOfAccount.objects.get(id=account).name
        if transaction_type == 'Credit':
            credit_sum = 0
            for item in obj:
                if item.debit == 0:
                    credit_sum += item.credit
            context = {
                'account': account_name,
                'type': transaction_type,
                'duration': start_month + ' to ' + end_month,
                'journal_items': obj,
                'chart_of_accounts': chart_of_accounts,
                'debit_sum': 0,
                'credit_sum': credit_sum,
                "nav": {
                    "parent_active": "reports",
                    "child_active": "account_statement", }
            }

            return render(request, "accounting/reports/account_statement.html", context)

        if transaction_type == 'Debit':
            debit_sum = 0
            for item in obj:
                if item.credit == 0:
                    debit_sum += item.debit
            context = {
                'account': account_name,
                'type': transaction_type,
                'duration': start_month + ' to ' + end_month,
                'journal_items': obj,
                'chart_of_accounts': chart_of_accounts,
                'debit_sum': debit_sum,
                'credit_sum': 0,
                "nav": {
                    "parent_active": "reports",
                    "child_active": "account_statement", }
            }

            return render(request, "accounting/reports/account_statement.html", context)

    if start_month and end_month and account == '' and transaction_type == '':
        obj = JournalItem.objects.filter(updated_at__range=[start_month, end_month])
        debit_sum = sum([item.debit for item in obj])
        credit_sum = sum([item.credit for item in obj])

        context = {
            'account': "All",
            'type': 'All',
            'duration': start_month + ' to ' + end_month,
            'journal_items': obj,
            'chart_of_accounts': chart_of_accounts,
            'debit_sum': debit_sum,
            'credit_sum': credit_sum, "nav": {
                "parent_active": "reports",
                "child_active": "account_statement", }
        }

        return render(request, "accounting/reports/account_statement.html", context)

    debit_sum = sum([item.debit for item in JournalItem.objects.all()])
    credit_sum = sum([item.credit for item in JournalItem.objects.all()])
    context = {
        'account': "All",
        'type': 'All',
        'duration': '_',

        'journal_items': journal_items,
        'chart_of_accounts': chart_of_accounts,
        'debit_sum': debit_sum,
        'credit_sum': credit_sum,
        "nav": {
            "parent_active": "reports",
            "child_active": "account_statement", }
    }

    return render(request, "accounting/reports/account_statement.html", context)


@login_required
def income_summary(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company
    year = request.GET.get('year')

    transactions_this_year = accounting_utils.expense_this_year(request, company, year)
    income_by_month = []
    income_by_reservation = []
    month_of_year = []
    for entry in transactions_this_year:
        income_by_month.append(entry.get('income'))
        income_by_reservation.append(entry.get('reservation_income'))
        month_of_year.append(entry.get('month_name'))

    res_lt = []  # declaration of the list
    for x in range(0, len(income_by_month)):
        res_lt.append(income_by_month[x] + income_by_reservation[x])

    context = {
        "nav": {
            "parent_active": "reports",
            "child_active": "income_summary", },
        'income_by_month': income_by_month,
        'month_of_year': month_of_year,
        'income_by_reservation': income_by_reservation,
        'total_income': res_lt,
        'year':year,
    }

    return render(request, "accounting/reports/income_summary.html", context)


@login_required
def expense_summary(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company
    year = request.GET.get('year')
    transactions_this_year = accounting_utils.expense_this_year(request, company, year)
    expense_by_month = []
    month_of_year = []
    for entry in transactions_this_year:
        expense_by_month.append(entry.get('expense'))
        month_of_year.append(entry.get('month_name'))
    context = {
        "nav": {
            "parent_active": "reports",
            "child_active": "expense_summary", },
        'expense_by_month': expense_by_month,
        'month_of_year': month_of_year,
        'year': year,
    }
    return render(request, "accounting/reports/expense_summary.html", context)


@login_required
def tax_summary(request):
    context = {
        "nav": {
            "parent_active": "reports",
            "child_active": "tax_summary", }
    }
    return render(request, "accounting/reports/tax_summary.html", context)


@login_required
def income_vs_expense_summary(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company
    year = request.GET.get('year')

    transactions_this_year = accounting_utils.expense_this_year(request, company, year)
    income_by_month = []
    income_by_reservation = []
    month_of_year = []
    expense_by_month = []
    for entry in transactions_this_year:
        income_by_month.append(entry.get('income'))
        income_by_reservation.append(entry.get('reservation_income'))
        expense_by_month.append(entry.get('expense'))
        month_of_year.append(entry.get('month_name'))

    res_lt = []  # declaration of the list
    for x in range(0, len(income_by_month)):
        res_lt.append(income_by_month[x] + income_by_reservation[x])

    profit_by_month = []  # declaration of the list
    for x in range(0, len(income_by_month)):
        profit_by_month.append(income_by_month[x] - expense_by_month[x])

    context = {
        "nav": {
            "parent_active": "reports",
            "child_active": "income_vs_expense_summary"},
        'income_by_month': income_by_month,
        'month_of_year': month_of_year,
        'income_by_reservation': income_by_reservation,
        'total_income': res_lt,
        'expense_by_month': expense_by_month,
        'profit_by_month': profit_by_month,
        'year': year,

    }

    return render(request, "accounting/reports/income_vs_expense_summary.html", context)


@login_required
def profit_loss_summary(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company
    year = request.GET.get('year')
    transactions_this_year = accounting_utils.expense_this_year(request, company, year)
    income_by_month = []
    income_by_reservation = []
    month_of_year = []
    expense_by_month = []
    for entry in transactions_this_year:
        income_by_month.append(entry.get('income'))
        income_by_reservation.append(entry.get('reservation_income'))
        expense_by_month.append(entry.get('expense'))
        month_of_year.append(entry.get('month_name'))

    res_lt = []  # declaration of the list
    for x in range(0, len(income_by_month)):
        res_lt.append(income_by_month[x])

    profit_by_month = []  # declaration of the list
    for x in range(0, len(income_by_month)):
        profit_by_month.append(income_by_month[x] - expense_by_month[x])

    context = {
        "nav": {
"parent_active": "reports",
            "child_active": "profit_loss_summary"},
        'income_by_month': income_by_month,
        'month_of_year': month_of_year,
        'income_by_reservation': income_by_reservation,
        'total_income': res_lt,
        'expense_by_month': expense_by_month,
        'profit_by_month': profit_by_month,
        'direct_income_sum': sum(income_by_month),
        'income_by_reservation_sum': sum(income_by_reservation),
        'total_income_sum': sum(res_lt),
        'direct_expense_sum': sum(expense_by_month),
        'profit_by_month_sum':sum(profit_by_month),
        'year': year,

    }

    return render(request, "accounting/reports/profit_loss_summary.html", context)


@login_required
def invoice_summary(request):
    context = {
        "nav": {
            "parent_active": "reports",
            "child_active": "invoice_summary", }
    }
    return render(request, "accounting/reports/invoice_summary.html", context)
