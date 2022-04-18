from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from ..DoubleEntry.models import ChartOfAccount
from ..Transaction.models import Transaction

from ..DoubleEntry import models as chart_of_account_model
from django.db.models import Q


@login_required
def bills(request):
    context = {

        "nav": {
            "parent_active": "expense",
            "child_active": "bills",
        },
    }
    return render(request, "accounting/expense/bill_index.html", context)


@login_required
def payments(request):
    context = {

        "nav": {
            "parent_active": "expense",
            "child_active": "payments",
        },
    }
    return render(request, "accounting/expense/payment_index.html", context)


@login_required
def add_bill(request):
    context = {

        "nav": {
            "parent_active": "expense",
            "child_active": "expense",
        },
    }
    return render(request, "accounting/expense/add_bill.html", context)


@login_required
def all_expense(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company

    all_transactions = Transaction.objects.filter(company=company)
    debit_sum = 0
    credit_sum = 0
    for transaction in all_transactions:
        if transaction.transaction_type == 'Deposit':
            debit_sum += transaction.amount
        else:
            credit_sum += transaction.amount
    # Transaction Accounts
    criterion_asset = Q(category='Cash and Bank')
    criterion_liability = Q(category='Other Short-Term Liability')
    criterion_equity = Q(category='Business Owner Contribution and Drawing')
    transaction_accounts = ChartOfAccount.objects.filter(criterion_asset | criterion_liability | criterion_equity)

    # Income Category Accounts
    criterion_asset = Q(category='Expected Payments from Customers')
    criterion_liability = Q(category='Expected Payments to Vendors')
    criterion_income_1 = Q(category='Income')
    criterion_income_2 = Q(category='Uncategorized Income')
    criterion_equity = Q(account_type='Equity')
    income_categories = ChartOfAccount.objects.filter(
        criterion_asset | criterion_liability | criterion_equity | criterion_income_1 | criterion_income_2)

    income_options = {
        'account_type': transaction_accounts,
        'transaction_type': 'Deposit',
        'category': income_categories,
    }

    criterion_asset = Q(category='Expected Payments from Customers')
    criterion_liability = Q(account_type='Liability')
    criterion_expense = Q(account_type='Expense')
    criterion_equity = Q(account_type='Equity')
    expense_categories = ChartOfAccount.objects.filter(
        criterion_asset | criterion_liability | criterion_equity | criterion_expense)

    expense_options = {
        'account_type': transaction_accounts,
        'transaction_type': 'Withdraw',
        'category': expense_categories,
    }

    context = {

        'income_options': income_options,
        'expense_options': expense_options,
        'all_transactions': all_transactions,
        "nav": {
            "parent_active": "expense",
            "child_active": "all_expenses",
        },
        'credit_sum': credit_sum,
    }

    return render(request, "accounting/expense/direct-expense.html", context)
