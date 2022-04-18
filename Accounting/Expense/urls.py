from django.urls import path, reverse
from . import views

urlpatterns = [

    path("bills", views.bills, name="bills"),
    path("payments", views.payments, name="payments"),
    path("bill-add", views.add_bill, name="bill-add"),
    path("expenses", views.all_expense, name="expenses"),


]
