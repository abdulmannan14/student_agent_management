from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from Employee import models as employee_model
from Client import models as client_models
from .Vendor import models as vendor_models
from .Transaction.models import Transaction
from .models import Asset
import datetime
from . import utils as accounting_utils
from .forms import AssetForm


@login_required
def dashboard(request):
    if request.user.userprofile.role == 'COMPANY':
        company = request.user.userprofile.companyprofilemodel
    else:
        company = request.user.userprofile.employeeprofilemodel.company
    clients = client_models.PersonalClientProfileModel.objects.filter(company=company)
    clients = company.personalclientprofilemodel_set.all()
    vendors = vendor_models.Vendor.objects.filter(company=company)

    income_today = accounting_utils.income_today(request, company)
    income_this_month = accounting_utils.income_this_month(request, company)
    expense_today = accounting_utils.expense_today(request, company)
    expense_this_month = accounting_utils.expense_this_month(request, company)
    transactions_this_year = accounting_utils.expense_this_year(request, company)

    chart_start_date = datetime.date.today()
    chart_end_date = chart_start_date - datetime.timedelta(days=15)
    all_transactions = Transaction.objects.filter(company=company,
                                                  dated__range=[chart_end_date, chart_start_date]).order_by('dated')
    latest_income = Transaction.objects.filter(transaction_type='Deposit').order_by('dated')[:10]
    latest_expense = Transaction.objects.filter(transaction_type='Withdraw').order_by('dated')[:10]
    latest_incomes = reversed(latest_income)
    latest_expenses = reversed(latest_expense)
    date_list = []
    income_list = []
    expense_list = []
    while chart_start_date >= chart_end_date:
        date_list.append(chart_start_date)
        deposit_data = all_transactions.filter(transaction_type='Deposit', dated=chart_start_date).values(
            "dated").order_by('dated').annotate(total_income=Sum('amount'))
        if deposit_data:
            income_list.append(deposit_data[0]['total_income'])
        else:
            income_list.append(0)

        expense_data = all_transactions.filter(transaction_type='Withdraw', dated=chart_start_date).values(
            "dated").order_by('dated').annotate(total_expense=Sum('amount'))
        if expense_data:
            expense_list.append(expense_data[0]['total_expense'])
        else:
            expense_list.append(0)
        chart_start_date -= datetime.timedelta(days=1)

    income_by_month = []

    expense_by_month = []
    month_of_year = []
    for entry in transactions_this_year:
        income_by_month.append(entry.get('income'))
        expense_by_month.append(entry.get('expense'))
        month_of_year.append(entry.get('month_name'))
    context = {
        'company': company,
        'clients': clients,
        'vendors': vendors,
        'all_transations': all_transactions,
        "nav": {
            "parent_active": "dashboard_cls",
            "child_active": "dashboard_cls",
        },
        'income_list': income_list[-50:],
        'expense_list': expense_list[-50:],
        'date_list': date_list[-50:],
        'income_today': income_today,
        'income_this_month': income_this_month,
        'expense_today': expense_today,
        'expense_this_month': expense_this_month,
        'income_by_month': income_by_month,
        'expense_by_month': expense_by_month,
        'month_of_year': month_of_year,
        'latest_incomes': latest_incomes,
        'latest_expenses': latest_expenses,

    }
    return render(request, "accounting/dashboard.html", context)


@login_required
def customers(request):
    try:
        company = request.user.userprofile.employeeprofilemodel.company.company
    except:
        company = request.user.userprofile.companyprofilemodel
    clients = client_models.PersonalClientProfileModel.objects.filter(company=company)
    context = {

        "clients": clients,
        "nav": {
            "parent_active": "clients_class",
            "child_active": "clients_class"},
    }

    return render(request, "accounting/customer_index.html", context)


@login_required
def employee(request):
    try:
        request_user_name = request.user.userprofile.employeeprofilemodel.company

    except:
        request_user_name = request.user.userprofile.companyprofilemodel
    employees = employee_model.EmployeeProfileModel.objects.filter(
        company__company_name=request_user_name)

    context = {
        "emoloyees": employees,
        "nav": {
            "parent_active": "staff_cls",
            "child_active": "employee_cls"},
    }
    return render(request, "accounting/employee.html", context)


@login_required
def assets(request):
    company = request.user.userprofile.companyprofilemodel
    all_assets = Asset.objects.filter(company=company)
    asset_form = AssetForm(request.POST or None)
    if request.method == 'POST':
        if asset_form.is_valid():
            asset = asset_form.save(commit=False)
            asset.company = company
            asset.save()
    context = {
        "asset_form": asset_form,
        'all_assets': all_assets,
        "nav": {
            "parent_active": "asset_class",
            "child_active": "asset_class"},
    }
    return render(request, "accounting/assets_index.html", context)


@login_required
def add_asset(request):
    company = request.user.userprofile.companyprofilemodel
    asset_form = AssetForm(request.POST or None)
    if request.method == 'POST':
        if asset_form.is_valid():
            asset = asset_form.save(commit=False)
            asset.company = company
            asset.save()
            messages.success(request, 'Asset Created Successfully!')
    return redirect("assets")


@login_required
def delete_asset(request, pk):
    asset = Asset.objects.get(pk=pk)
    asset.delete()
    messages.success(request, 'Asset Deleted !')
    return redirect("assets")


@login_required
def edit_asset(request, pk):
    company = request.user.userprofile.companyprofilemodel
    all_assets = Asset.objects.filter(company=company)
    asset = Asset.objects.get(pk=pk)
    if request.method == 'POST':
        asset.name = request.POST.get('name')
        asset.amount = request.POST.get('amount')
        asset.purchase_date = request.POST.get('purchase_date')
        asset.supported_date = request.POST.get('supported_date')
        asset.description = request.POST.get('description')
        asset.save()
        messages.success(request, 'Asset Updated Successfully!')
        return redirect("assets")
    else:
        context = {
            "asset": asset,
            'all_assets': all_assets
        }
    form_html = render_to_string("accounting/edit_asset_form.html", context, request)
    return JsonResponse(form_html, safe=False)
