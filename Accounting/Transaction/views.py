from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Transaction
from django.db.models import Q
from django.contrib import messages

# from .models import ChartOfAccount
from ..DoubleEntry.models import ChartOfAccount, JournalEntry, JournalItem


@login_required
def all_transactions(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company.company

    all_transactions = Transaction.objects.filter(company=company)
    debit_sum = 0
    credit_sum = 0
    for transaction in all_transactions:
        if transaction.transaction_type == 'Deposit':
            debit_sum += transaction.amount
        else:
            credit_sum += transaction.amount
    # debit_sum = sum([item.debit for item in JournalItem.objects.all()])

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
            "parent_active": "reports",
            "child_active": "transactions",
        },
        'credit_sum': credit_sum,
        'debit_sum': debit_sum
    }

    return render(request, "accounting/transactions/transactions.html", context)


@login_required
def add_transaction(request):
    if request.method == "POST":
        dated = request.POST.get('dated')
        amount = request.POST.get('amount')
        account_type = request.POST.get('account_type')
        transaction_type = request.POST.get('transaction_type')
        category = request.POST.get('category')
        description = request.POST.get('description')

        if request.user.userprofile.role == 'COMPANY':
            company = request.user.userprofile.companyprofilemodel
        else:
            company = request.user.userprofile.employeeprofilemodel.company.company

        account_type_obj = ChartOfAccount.objects.get(name=account_type)
        category_obj = ChartOfAccount.objects.get(name=category)

        transaction_obj = Transaction.objects.create(dated=dated, amount=amount, account_type=account_type_obj,
                                                     transaction_type=transaction_type, category=category_obj,
                                                     description=description,
                                                     company=company)

        messages.success(request , 'Transaction Successfully Completed !')

        if transaction_type == 'Withdraw':
            journal_entry_obj = JournalEntry.objects.create(dated=dated, journal_no='EXPENSE_00001',
                                                            description='Direct Expense - ' + description,
                                                            company=company,
                                                            transaction=transaction_obj)
            # Asset Account Reduction
            JournalItem.objects.create(journal_entry=journal_entry_obj, account=account_type_obj, credit=amount,
                                       company=company)
            # Expense Account Addition
            JournalItem.objects.create(journal_entry=journal_entry_obj, account=category_obj, debit=amount,
                                       company=company)

        elif transaction_type == 'Deposit':
            journal_entry_obj = JournalEntry.objects.create(dated=dated, journal_no='INCOME_00001',
                                                            description='Direct Income - ' + description,
                                                            company=company,
                                                            transaction=transaction_obj)
            # Asset Account Addition
            JournalItem.objects.create(journal_entry=journal_entry_obj, account=account_type_obj, debit=amount,
                                       company=company)
            # Expense Account Reduction
            JournalItem.objects.create(journal_entry=journal_entry_obj, account=category_obj, credit=amount,
                                       company=company)

    return redirect('all-transactions')


def edit_transaction(request, pk):
    transaction = Transaction.objects.get(pk=pk)
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
    if request.method == "POST":
        account_type = request.POST.get('account_type')
        category = request.POST.get('category')
        account_type_obj = ChartOfAccount.objects.get(name=account_type)
        category_obj = ChartOfAccount.objects.get(name=category)
        transaction.dated = request.POST.get('dated')
        amount = request.POST.get('amount')
        transaction.amount = amount
        transaction.account_type = account_type_obj
        transaction.transaction_type = request.POST.get('transaction_type')
        transaction.category = category_obj
        transaction.description = request.POST.get('description')
        transaction.save()
        journal_entry_obj = transaction.journalentry_set.first()
        if journal_entry_obj:
            journal_entry_obj.dated = request.POST.get('dated')
            journal_entry_obj.description = 'Direct Expense - ' + request.POST.get('description')
            journal_entry_obj.save()
        journal_item_obj = journal_entry_obj.journalitem_set.all()
        for item_objects in journal_item_obj:
            if request.POST.get('transaction_type') == 'Withdraw':
                if item_objects.credit == 0:
                    item_objects.account = category_obj
                    item_objects.debit = amount
                    item_objects.save()
                elif item_objects.debit == 0:
                    item_objects.account = account_type_obj
                    item_objects.credit = amount
                    item_objects.save()
            elif request.POST.get('transaction_type') == 'Deposit':
                if item_objects.credit == 0:
                    item_objects.account = account_type_obj
                    item_objects.debit = amount
                    item_objects.save()
                elif item_objects.debit == 0:
                    item_objects.account = category_obj
                    item_objects.credit = amount
                    item_objects.save()
        messages.success(request, "Transaction Updated")
        return redirect('all-transactions')
    else:
        context = {
            'transaction': transaction,
            'income_options': income_options,
            'expense_options': expense_options,

        }
        form_html = render_to_string("accounting/transactions/edit_transaction_form.html", context, request)
        return JsonResponse(form_html, safe=False)


@login_required
def delete_transaction(request, pk):
    transaction = Transaction.objects.get(pk=pk)
    transaction.delete()
    messages.success(request, "Transaction Deleted")
    return redirect('all-transactions')
