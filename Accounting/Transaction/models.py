from django.db import models
from Company import models as company_models
from Client import models as client_models
from Reservation import models as reservation_models
from Accounting.Vendor import models as vendor_models


class Transaction(models.Model):
    DEPOSIT = "Deposit"
    WITHDRAW = "Withdraw"

    types = [
        (DEPOSIT, DEPOSIT),
        (WITHDRAW, WITHDRAW),

    ]
    dated = models.DateField(null=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    account_type = models.ForeignKey('Accounting.ChartOfAccount', on_delete=models.CASCADE, null=True)
    transaction_type = models.CharField(max_length=40, null=True, blank=True, choices=types)
    amount = models.FloatField(blank=True, null=True)
    category = models.ForeignKey('Accounting.ChartOfAccount', on_delete=models.CASCADE, null=True,
                                 related_name="transaction_category")
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(vendor_models.Vendor, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(client_models.PersonalClientProfileModel, on_delete=models.CASCADE, null=True)
    reservation = models.ForeignKey(reservation_models.Reservation, on_delete=models.CASCADE, null=True)
    bill = models.ForeignKey(vendor_models.Bill, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
