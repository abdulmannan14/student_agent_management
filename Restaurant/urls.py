from django.urls import path, reverse
from . import views as restaurant_views, views_customer as customer_view

urlpatterns = [
    path('expenses/all', restaurant_views.all_expenses, name='restaurant-all-expenses'),
    path('overview', restaurant_views.restaurant_overview, name='restaurant-overview'),
    path('add', restaurant_views.add_expense, name='restaurant-add-expense'),
    path('edit/<int:pk>', restaurant_views.edit_expense, name='restaurant-edit-expense'),
    path('delete/<int:pk>', restaurant_views.delete_expense, name='restaurant-delete-expense'),
    path('expenses/today', restaurant_views.today_expense, name='restaurant-today-expense'),
    # ============================ORDER VIEW====================================
    path('customer/end/main', customer_view.customer_main_view, name='restaurant-customer-main-view'),
    path('customer/end/get_bill', customer_view.get_bill, name='get-bill'),
]


def all_expense():
    return reverse("restaurant-all-expenses")


def add_expense():
    return reverse("restaurant-add-expense")


def edit_expense(pk: int):
    return reverse("restaurant-edit-expense", kwargs={"pk": pk})


def delete_expense(pk: int):
    return reverse("restaurant-delete-expense", kwargs={"pk": pk})
