from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from Account.models import UserProfile
from Company import models as company_models
from setting import models as setting_models


class Vendor(models.Model):
    REGULAR = "REGULAR"
    INDIVIDUAL = "INDIVIDUAL"
    CONTRACTOR = "CONTRACTOR"
    types = [
        (REGULAR, REGULAR),
        (INDIVIDUAL, INDIVIDUAL),
        (CONTRACTOR, CONTRACTOR)
    ]

    vendor_type = models.CharField(max_length=40, null=True, blank=True, choices=types)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    billing_name = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    billing_phone = models.CharField(max_length=20, null=True, blank=True)
    zip = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    balance = models.FloatField(null=True, blank=True, default=0)
    ssn = models.CharField(max_length=20, null=True, blank=True)
    ein = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Bill(models.Model):
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    bill_number = models.CharField(max_length=50, null=True, blank=True)
    bill_date = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey('Accounting.ChartOfAccount', on_delete=models.CASCADE, null=True)
    sales_tax = models.ForeignKey(setting_models.SalesTax, on_delete=models.CASCADE, null=True)
    item = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
