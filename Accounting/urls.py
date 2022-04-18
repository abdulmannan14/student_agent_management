from django.urls import path, reverse, include
from . import views as accounting_views

urlpatterns = [

    path("dashboard", accounting_views.dashboard, name="accounting-dashboard"),
    path("customer-index", accounting_views.customers, name="customers-index"),
    path("emlployee", accounting_views.employee, name="employee"),

    path("assets", accounting_views.assets, name="assets"),
    path("add-asset", accounting_views.add_asset, name="add-asset"),
    path("delete-asset/<int:pk>", accounting_views.delete_asset, name="delete-asset"),
    path("edit-asset/<int:pk>", accounting_views.edit_asset, name="edit-asset"),

    path("vendor/", include("Accounting.Vendor.urls")),
    path("double-entry/", include("Accounting.DoubleEntry.urls")),
    path("expense/", include("Accounting.Expense.urls")),
    path("report/", include("Accounting.Report.urls")),
    path("transaction/", include("Accounting.Transaction.urls")),
    path("income/", include("Accounting.Income.urls")),

]
