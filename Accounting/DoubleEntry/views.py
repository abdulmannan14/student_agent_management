from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from .models import ChartOfAccount, JournalEntry, JournalItem

from . import urls as double_entry_urls
from . import forms as double_entry_forms
from . import utils as double_entry_utils
from .tables import JournalEntryTable
from django.db.models import Q, Sum

from .. import Expense
from django.contrib import messages

@login_required
def chart_of_accounts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        category = request.POST.get("category")
        account_type = request.POST.get("account_type")
        description = request.POST.get("description")
        if request.POST.get("is_enabled") == "on":
            is_enabled = True
        else:
            is_enabled = False

        ChartOfAccount.objects.create(name=name, code=code, account_type=account_type, category=category,
                                      is_enabled=is_enabled,
                                      description=description)
        return redirect("chart-of-accounts")
    elif request.method == "GET":

        accounts = ChartOfAccount.objects.all()
        db_options = ChartOfAccount.types
        account_types = []
        for option in db_options:
            account_types.append(option[0])
        account_categories = []
        db_options = ChartOfAccount().get_account_categories('Asset')
        for option in db_options:
            account_categories.append(option[0])
        context = {
            "nav": {
                "parent_active": "double-entries",
                "child_active": "chart_of_accounts",
            },
            'accounts': accounts,
            'account_types': account_types,
            "account_categories": account_categories,

        }

        return render(request, "accounting/double_entry/chart_of_accounts.html", context)


def get_account_type_categories(request):
    account_type = request.GET.get("account_type", "")
    chart_of_account = ChartOfAccount()
    categories = chart_of_account.get_account_categories(account=account_type)
    options = [option[0] for option in categories]
    return JsonResponse(options, safe=False)


@login_required
def delete_chart_of_accounts(request, pk):
    account = ChartOfAccount.objects.get(pk=pk)
    account.delete()
    messages.success(request, 'Account Deleted !')
    return redirect('chart-of-accounts')


@login_required
def edit_chart_of_accounts(request, pk):
    account = ChartOfAccount.objects.get(pk=pk)
    account_categories = []
    db_options = ChartOfAccount().get_account_categories('Asset')
    for option in db_options:
        account_categories.append(option[0])
    if request.method == "POST":
        account.name = request.POST.get("name")
        account.code = request.POST.get("code")
        account.account_type = request.POST.get("account_type")
        account.description = request.POST.get("description")
        account.category = request.POST.get("category")
        if request.POST.get("is_enabled") == "on":
            account.is_enabled = True
        else:
            account.is_enabled = False
        account.save()
        messages.success(request, 'Account Updated !')

        return redirect("chart-of-accounts")
    else:
        context = {
            'account': account,
            'account_categories': account_categories,
        }
        form_html = render_to_string("accounting/double_entry/edit_account_form.html", context, request)
        return JsonResponse(form_html, safe=False)


@login_required
def balance_sheet(request):
    company = request.user.userprofile.companyprofilemodel
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    chart_of_accounts_obj = ChartOfAccount.objects.filter(company=company)
    journal_items_obj = JournalItem.objects.filter(company=company)
    if start_date and end_date:
        date_range = Q(updated_at__range=[start_date, end_date])
        chart_of_accounts = chart_of_accounts_obj.filter(date_range)
        journal_items = journal_items_obj.filter(date_range)
    else:
        chart_of_accounts = chart_of_accounts_obj
        journal_items = journal_items_obj
    categories = ChartOfAccount.categories
    account_detail_list = []
    for category in categories:
        accounts = chart_of_accounts.filter(category=category[1])
        for account in accounts:
            j_items = journal_items.filter(account=account)
            cash_bank_sum = 0
            for j_item in j_items:
                if j_item.account.account_type == ChartOfAccount.ASSET or j_item.account.account_type == ChartOfAccount.EXPENSE:
                    cash_bank_sum += j_item.debit
                    cash_bank_sum -= j_item.credit
                elif j_item.account.account_type == ChartOfAccount.LIABILITY or j_item.account.account_type == ChartOfAccount.EQUITY or j_item.account.account_type == ChartOfAccount.INCOME:
                    cash_bank_sum += j_item.credit
                    cash_bank_sum -= j_item.debit

            account_detail_list.append({
                'account': account.name,
                'amount': cash_bank_sum,
                'type': account.account_type,
                'category': account.category
            })

            # sum by category
    operating_expense_sum = 0
    for item in account_detail_list:
        if item.get('category') == 'Operating Expense':
            operating_expense_sum += item.get('amount')

    payroll_expense_sum = 0
    for item in account_detail_list:
        if item.get('category') == 'Payroll Expense':
            payroll_expense_sum += item.get('amount')

    uncategorized_expense = 0
    for item in account_detail_list:
        if item.get('category') == 'Uncategorized Expense':
            uncategorized_expense += item.get('amount')

    income = 0
    for item in account_detail_list:
        if item.get('category') == 'Income':
            income += item.get('amount')

    uncategorized_income = 0
    for item in account_detail_list:
        if item.get('category') == 'Uncategorized Income':
            uncategorized_income += item.get('amount')

    contribution_and_drawing = 0
    for item in account_detail_list:
        if item.get('category') == 'Business Owner Contribution and Drawing':
            contribution_and_drawing += item.get('amount')
    retained_earnings = 0
    for item in account_detail_list:
        if item.get('category') == 'Retained Earnings: Profit':
            retained_earnings += item.get('amount')
    payments_to_vendors = 0
    for item in account_detail_list:
        if item.get('category') == 'Expected Payments to Vendors':
            payments_to_vendors += item.get('amount')
    sales_taxes = 0
    for item in account_detail_list:
        if item.get('category') == 'Sales Taxes':
            sales_taxes += item.get('amount')
    due_for_payroll = 0
    for item in account_detail_list:
        if item.get('category') == 'Due for Payroll':
            due_for_payroll += item.get('amount')
    short_term_liability = 0
    for item in account_detail_list:
        if item.get('category') == 'Other Short-Term Liability':
            short_term_liability += item.get('amount')

    cash_bank = 0
    for item in account_detail_list:
        if item.get('category') == 'Cash and Bank':
            cash_bank += item.get('amount')
    payment_from_customers = 0
    for item in account_detail_list:
        if item.get('category') == 'Expected Payments from Customers':
            payment_from_customers += item.get('amount')

            # sum by types

    total_asset = 0
    for item in account_detail_list:
        if item.get('type') == 'Asset':
            total_asset += item.get('amount')

    total_liability = 0
    for item in account_detail_list:
        if item.get('type') == 'Liability':
            total_liability += item.get('amount')
    total_expense = 0
    for item in account_detail_list:
        if item.get('type') == 'Expense':
            total_expense += item.get('amount')
    total_income = 0
    for item in account_detail_list:
        if item.get('type') == 'Income':
            total_income += item.get('amount')
    total_equity = 0
    for item in account_detail_list:
        if item.get('type') == 'Equity':
            total_equity += item.get('amount')
    context = {
        "nav": {
            "parent_active": "double-entries",
            "child_active": "balance_sheet",
        },
        'account_list': account_detail_list,
        'operating_expense_sum': operating_expense_sum,
        'payroll_expense_sum': payroll_expense_sum,
        'uncategorized_expense': uncategorized_expense,
        'income': income,
        'uncategorized_income': uncategorized_income,
        'contribution_and_drawing': contribution_and_drawing,
        'retained_earnings': retained_earnings,
        'payments_to_vendors': payments_to_vendors,
        "sales_taxes": sales_taxes,
        'due_for_payroll': due_for_payroll,
        'short_term_liability': short_term_liability,
        'cash_bank': cash_bank,
        'payment_from_customers': payment_from_customers,
        'total_asset': total_asset,
        'total_liability': total_liability,
        'total_expense': total_expense,
        'total_income': total_income,
        'total_equity': total_equity,
        'start_date': start_date,
        'end_date': end_date,

    }
    return render(request, "accounting/double_entry/balance_sheet.html", context)


@login_required
def ledger_summary(request):
    company = request.user.userprofile.companyprofilemodel
    journal_items = JournalItem.objects.filter(company=company)
    chart_of_accounts = ChartOfAccount.objects.filter(company=company)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    account = request.GET.get('account')
    if account:
        accounts_name = ChartOfAccount.objects.get(id=account).name
        journal_items = journal_items.filter(account=account)
    else:
        accounts_name = 'ALL'
    if start_date and end_date:
        journal_items = journal_items.filter(updated_at__range=[start_date, end_date])
    debit_sum = sum([item.debit for item in journal_items])
    credit_sum = sum([item.credit for item in journal_items])
    balance_sum = debit_sum - credit_sum
    temp_sum = 0
    ledger = []
    balance = []

    if len(journal_items) != 0:
        temp_entry = journal_items[0].journal_entry
    for item in journal_items:
        if temp_entry != item.journal_entry:
            temp_entry = item.journal_entry
            temp_sum = 0
        temp_sum += item.debit
        temp_sum -= item.credit
        balance.append(temp_sum)
        temp_dict = {
            'item': item,
            'balance': temp_sum
        }
        ledger.append(temp_dict)

    context = {
        "nav": {
            "parent_active": "double-entries",
            "child_active": "ledger_summary",
        },
        'journal_items': ledger,
        'chart_of_accounts': chart_of_accounts,
        'debit_sum': debit_sum,
        'credit_sum': credit_sum,
        'balance': balance_sum,
        'account': accounts_name,
        "start_date": start_date,
        "end_date": end_date
    }
    return render(request, "accounting/double_entry/ledger_summary.html", context)


@login_required
def trial_balance(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company

    obj = JournalItem.objects.filter(company=company)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        date_range = Q(updated_at__range=[start_date, end_date])
        company = Q(company=company)
        obj_item = JournalItem.objects.filter(company)
        obj = obj_item.filter(date_range)
        total_debit = obj.values("account").annotate(total_debit=Sum('debit'))
        total_credit = obj.values("account").annotate(total_credit=Sum('credit'))
        all_accounts = ChartOfAccount.objects.all()
        trial_accounts = []
        for index, item in enumerate(total_debit):
            if total_credit[index]['total_credit'] > 0 or total_debit[index]['total_debit'] > 0:
                account_name = all_accounts.get(pk=item['account']).name
                trial_accounts.append({
                    'account': account_name,
                    'debit': total_debit[index]['total_debit'],
                    'credit': total_credit[index]['total_credit'],
                })
        credit_sum = sum([item.get('credit') for item in trial_accounts])
        debit_sum = sum([item.get('debit') for item in trial_accounts])
        context = {
            "nav": {
                "parent_active": "double-entries",
                "child_active": "trial_balance",
            },
            'trial_accounts': trial_accounts,
            'credit_sum': credit_sum,
            'debit_sum': debit_sum,
            'start_date': start_date,
            'end_date': end_date,

        }
        return render(request, "accounting/double_entry/trial_balance.html", context)
    else:
        total_debit = obj.values("account").annotate(total_debit=Sum('debit'))
        total_credit = obj.values("account").annotate(total_credit=Sum('credit'))
        all_accounts = ChartOfAccount.objects.all()
        trial_accounts = []
        for index, item in enumerate(total_debit):
            if total_credit[index]['total_credit'] > 0 or total_debit[index]['total_debit'] > 0:
                account_name = all_accounts.get(pk=item['account']).name
                trial_accounts.append({
                    'account': account_name,
                    'debit': total_debit[index]['total_debit'],
                    'credit': total_credit[index]['total_credit'],
                })
        credit_sum = sum([item.get('credit') for item in trial_accounts])
        debit_sum = sum([item.get('debit') for item in trial_accounts])
        context = {
            "nav": {
                "parent_active": "double-entries",
                "child_active": "trial_balance",
            },
            'trial_accounts': trial_accounts,
            'credit_sum': credit_sum,
            'debit_sum': debit_sum,

        }
        return render(request, "accounting/double_entry/trial_balance.html", context)


@login_required
def journal_entry_details(request, pk):
    je = JournalEntry.objects.get(pk=pk)
    debit_sum = sum([item.debit for item in je.journalitem_set.all()])
    credit_sum = sum([item.credit for item in je.journalitem_set.all()])

    context = {
        'journal_entry': je,
        'debit_sum': debit_sum,
        'credit_sum': credit_sum,
        "nav": {
            "parent_active": "double-entries",
            "child_active": "ledger_summary",
        },
    }
    return render(request, "accounting/double_entry/journal_entry_details.html", context)


@login_required
def journal_entry(request):
    company = request.user.userprofile.companyprofilemodel
    journal_entries = JournalEntry.objects.filter(company=company)
    table = JournalEntryTable(journal_entries)
    context = {
        'table': table,
        "nav": {
            "parent_active": "double-entries",
            "child_active": "journal-entries"
        }

    }
    return render(request, "accounting/double_entry/journal_entry.html", context)


@login_required
def add_journal_entry(request):
    # je = JournalEntry.objects.last
    company = request.user.userprofile.companyprofilemodel
    chart_of_accounts = ChartOfAccount.objects.filter(company=company)
    journal_entry_form = double_entry_forms.JournalEntryForm(request.POST or None)
    journal_item_form = double_entry_forms.JournalItemForm()
    if request.method == "POST":
        if journal_entry_form.is_valid():  # and other_for.is_valid
            post_data = request.POST.dict()
            accounts = double_entry_utils.parse_dict(post_data)
            journal_entry = double_entry_utils.create_journal_entry(journal_entry_form, company)
            double_entry_utils.create_journal_items(accounts, journal_entry)
            messages.success(request, 'Journal Entry Created !')

    else:
        pass

        # journal_entry_form.fields["journal_no"].initial = "1234455"
    journal_item_forms = [journal_item_form]
    context = {
        "journal_entry_form": journal_entry_form,
        "chart_of_accounts": chart_of_accounts,
        "journal_item_forms": journal_item_forms,
        "journal_item_form_labels": [field.label for field in journal_item_forms[0]],
        "nav": {
            "parent_active": "double-entries",
            "child_active": "journal-entries"
        }
    }

    return render(request, "accounting/double_entry/add_journal_entry.html", context)


@login_required
def edit_journal_entry(request, pk):
    je = JournalEntry.objects.get(pk=pk)
    company = request.user.userprofile.companyprofilemodel
    chart_of_accounts = ChartOfAccount.objects.filter(company=company)
    journal_entry_form = double_entry_forms.JournalEntryForm(request.POST or None, instance=je)
    # for jei in je.journalitem_set.all():

    journal_item_forms = [double_entry_forms.JournalItemForm(instance=jei) for jei in je.journalitem_set.all()]
    if request.method == "POST":
        if journal_entry_form.is_valid():  # and other_for.is_valid
            post_data = request.POST.dict()
            accounts = double_entry_utils.parse_dict(post_data)
            journal_entry = double_entry_utils.create_journal_entry(journal_entry_form, company)
            double_entry_utils.create_journal_items(accounts, journal_entry)

    else:
        pass

        # journal_entry_form.fields["journal_no"].initial = "1234455"
    context = {
        "journal_entry_form": journal_entry_form,
        "chart_of_accounts": chart_of_accounts,
        "journal_item_forms": journal_item_forms,
        "journal_item_form_labels": [field.label for field in journal_item_forms[0]]
    }

    return render(request, "accounting/double_entry/add_journal_entry.html", context)


@login_required
def delete_journal_entry(request, pk):
    journal_entry = JournalEntry.objects.get(pk=pk)
    journal_entry.delete()
    messages.success(request, 'Journal Entry Deleted !')

    return redirect('journal-entry')

