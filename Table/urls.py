from django.urls import path, reverse
from . import views as table_views

urlpatterns = [
    path('', table_views.all_tables, name='restaurant-all-table'),
    path('add', table_views.add_table, name='restaurant-add-table'),
    path('edit/<int:pk>', table_views.edit_table, name='restaurant-edit-table'),
    path('delete/<int:pk>', table_views.delete_table, name='restaurant-delete-table'),
    # path('overview/<int:pk>', table_views.overview_table, name='restaurant-overview-table'),
]




def all_table():
    return reverse("restaurant-all-table")


def add_table():
    return reverse("restaurant-add-table")


def edit_table(pk: int):
    return reverse("restaurant-edit-table", kwargs={"pk": pk})


def delete_table(pk: int):
    return reverse("restaurant-delete-table", kwargs={"pk": pk})


# def table_overview(pk: int):
#     return reverse("restaurant-overview-table", kwargs={"pk": pk})

