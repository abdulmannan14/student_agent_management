from django.db import models
from Company import models as company_models
from datetime import date


# class SalesTax(models.Model):
#     company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
#     name = models.CharField(max_length=50, null=True, blank=True)
#     abbreviation = models.CharField(max_length=50, null=True, blank=True)
#     description = models.TextField(max_length=1000, null=True, blank=True)
#     tax_number = models.CharField(max_length=50, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True)
#
#
# class TaxRate(models.Model):
#     company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
#     sales_tax = models.ForeignKey(SalesTax, on_delete=models.CASCADE, null=True)
#     rate = models.FloatField(null=True, blank=True, default=0)
#     effective_date = models.DateField(default=date(day=1, month=1, year=1900), null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True)
