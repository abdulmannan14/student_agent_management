from django.db import models
from datetime import datetime

from Company.models import CompanyAddressModel


def _get_months_in_years():
    months = [("", "MM")]
    [months.append((month, month)) for month in range(1, 13)]
    return months


def _get_years_from_now(years_ahead=0):
    current_year = datetime.now().year
    years = [("", "YYYY")]
    [years.append((current_year + itr, current_year + itr)) for itr in range(0, years_ahead)]
    return years


class PaymentInfo(models.Model):
    card_holder_name = models.CharField(max_length=100, null=True, blank=False)
    card_number = models.CharField(max_length=16, null=True, blank=False)
    expiry_month = models.IntegerField(null=True, blank=False, choices=_get_months_in_years(),
                                       help_text="Expiry month")
    expiry_year = models.IntegerField(null=True, blank=False,
                                      choices=_get_years_from_now(years_ahead=15), help_text="Expiry year")
    security_code = models.CharField(max_length=3, null=True, blank=False, help_text="CVV")

    # address = models.ForeignKey(CompanyAddressModel, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.card_holder_name
