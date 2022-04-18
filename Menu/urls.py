from django.urls import path, reverse
from . import views as menu_views

urlpatterns = [
    path('head', menu_views.all_menu_head, name='restaurant-all-menu-head'),
    path('head/add', menu_views.add_menu_head, name='restaurant-add-menu-head'),
    path('head/edit/<int:pk>', menu_views.edit_menu_head, name='restaurant-edit-menu-head'),
    path('head/delete/<int:pk>', menu_views.delete_menu_head, name='restaurant-delete-menu-head'),
    # ====================================================================================================
    path('items', menu_views.all_menu_items, name='restaurant-all-menu-item'),
    path('items/add', menu_views.add_menu_items, name='restaurant-add-menu-item'),
    path('items/edit/<int:pk>', menu_views.edit_menu_items, name='restaurant-edit-menu-item'),
    path('items/delete/<int:pk>', menu_views.delete_menu_items, name='restaurant-delete-menu-item'),
]


def all_menu_head():
    return reverse("restaurant-all-menu-head")


def add_menu_head():
    return reverse("restaurant-add-menu-head")


def edit_menu_head(pk: int):
    return reverse("restaurant-edit-menu-head", kwargs={"pk": pk})


def delete_menu_head(pk: int):
    return reverse("restaurant-delete-menu-head", kwargs={"pk": pk})

# ===================================================================================


def all_menu_item():
    return reverse("restaurant-all-menu-item")


def add_menu_item():
    return reverse("restaurant-add-menu-item")


def edit_menu_item(pk: int):
    return reverse("restaurant-edit-menu-item", kwargs={"pk": pk})


def delete_menu_item(pk: int):
    return reverse("restaurant-delete-menu-item", kwargs={"pk": pk})