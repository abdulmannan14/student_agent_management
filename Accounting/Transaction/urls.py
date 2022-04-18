from django.urls import path, reverse
from . import views

urlpatterns = [

    path("all", views.all_transactions, name="all-transactions"),
    path("add", views.add_transaction, name="add-transaction"),
    path("<int:pk>/edit", views.edit_transaction, name="edit-transaction"),
    path("<int:pk>/delete", views.delete_transaction, name="delete-transaction"),

]
