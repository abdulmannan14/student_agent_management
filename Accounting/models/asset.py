from django.db import models
from Company import models as company_models


class Asset(models.Model):
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True, default=0)
    description = models.TextField(max_length=1000, null=True, blank=True)
    purchase_date = models.DateField(null=True)
    supported_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
