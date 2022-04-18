from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from .utils import stripe_reservation_payment
from ..DoubleEntry.models import ChartOfAccount
from ..Transaction.models import Transaction
from Reservation.models import Reservation
from .tables import ReservationTable
from ..DoubleEntry import models as chart_of_account_model
from django.db.models import Q
from ..DoubleEntry import utils as double_entry_utils
from django.contrib import messages


@login_required
def direct_income(request):
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
            "parent_active": "income",
            "child_active": "credit_notes",
        },
        'debit_sum': debit_sum

    }

    return render(request, "accounting/income/direct-income.html", context)


@login_required
def reservations(request):
    try:
        company = request.user.userprofile.employeeprofilemodel.company
    except:
        company = request.user.userprofile.companyprofilemodel
    all_reservations = Reservation.objects.filter(company=company)
    payment_accounts = ChartOfAccount.objects.filter(company=company, category=ChartOfAccount.CASH_BANK)
    table = ReservationTable(all_reservations)
    context = {
        'table': table,
        "nav": {
            "parent_active": "income",
            "child_active": "all_reservation",

        },
        'payment_accounts': payment_accounts,

    }

    return render(request, "accounting/income/reservations.html", context)


@login_required
def reservation_payment(request):
    try:
        company = request.user.userprofile.employeeprofilemodel.company
    except:
        company = request.user.userprofile.companyprofilemodel
    account = request.POST.get('account')
    reservation_id = request.POST.get('reservation_id')
    amount = request.POST.get('amount')
    dated = request.POST.get('dated')
    reservation = Reservation.objects.filter(company=company, pk=reservation_id).first()

    if float(amount) > reservation.balance_fare:
        messages.error(request, "Payment exceeds balance amount of reservation.")
    elif float(amount) < 1:
        messages.error(request, "Payment amount is too low.")
    else:

        # For Payment by Cash
        if account == ChartOfAccount.COH:
            double_entry_utils.journal_entry_payment(reservation, amount, dated, account)
            if float(amount) == reservation.balance_fare:
                reservation.balance_paid = True
            reservation.balance_fare -= float(amount)
            reservation.save()
            messages.success(request, "Payment Successful!")
        # For Payment via Stripe Credit Card
        else:
            payment_response = stripe_reservation_payment(reservation.client, amount)
            if payment_response is True:
                double_entry_utils.journal_entry_payment(reservation, amount, dated, account)
                if float(amount) == reservation.balance_fare:
                    reservation.balance_paid = True
                reservation.balance_fare -= float(amount)
                reservation.save()
                messages.success(request, "Payment Successful!")
            elif payment_response is False:
                messages.error(request, "Transaction Failure.")
            elif payment_response is None:
                messages.error(request, "No Payment Method Attached for Client.")

    return redirect('reservations')
