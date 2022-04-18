from django.urls import path, reverse
from . import views

urlpatterns = [

    path("transactions", views.transactions, name="transactions"),
    path("account-statement", views.account_statement, name="account-statement"),
    path("income-summary", views.income_summary, name="income-summary"),
    path("expense-summary", views.expense_summary, name="expense-summary"),
    path("tax-summary", views.tax_summary, name="tax-summary"),
    path("invoice-summary", views.invoice_summary, name="invoice-summary"),
    path("income-vs-expense-summary", views.income_vs_expense_summary, name="income-vs-expense-summary"),
    path("profit-loss-summary", views.profit_loss_summary, name="profit-loss-summary"),

]
