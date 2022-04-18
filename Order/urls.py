

from django.urls import path, reverse
from . import views as order_views

urlpatterns = [
    path('', order_views.all_orders, name='restaurant-all-orders'),
    path('today', order_views.today_orders, name='restaurant-today-orders'),
    path('add', order_views.add_order, name='restaurant-add-order'),
    path('edit/<int:pk>', order_views.edit_order, name='restaurant-edit-order'),
    path('delete/<int:pk>', order_views.delete_order, name='restaurant-delete-order'),
    path('feedback', order_views.feedback_order, name='restaurant-feedback-order'),
    path('feedback/today', order_views.today_feedback_order, name='restaurant-today-feedback'),
]




def all_order():
    return reverse("restaurant-all-order")


def add_order():
    return reverse("restaurant-add-order")


def edit_order(pk: int):
    return reverse("restaurant-edit-order", kwargs={"pk": pk})


def delete_order(pk: int):
    return reverse("restaurant-delete-order", kwargs={"pk": pk})


# def order_overview(pk: int):
#     return reverse("restaurant-overview-order", kwargs={"pk": pk})

