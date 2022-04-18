from django.urls import path, reverse
from . import views

urlpatterns = [

    path("", views.vendors, name="vendors"),
    path("add", views.add_vendor, name="vendor-add"),
    path("create-vendor-bill", views.vendor_bills, name="create-vendor-bill"),

    path("<int:pk>/detail", views.get_vendor_detail, name="vendor-detail"),
    path("<int:pk>/edit", views.edit_vendor, name="vendor-edit"),
    path("<int:pk>/delete", views.delete_vendor, name="vendor-delete"),
    path("vendor2", views.vendors2, name="vendors2"),

]


def all_vendors():
    return reverse("vendors")


def vendor_details(pk: int):
    return reverse("vendor-detail", kwargs={"pk": pk})


def create_vendors():
    return reverse("vendor-add")
