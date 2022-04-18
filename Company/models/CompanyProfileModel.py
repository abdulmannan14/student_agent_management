import datetime

import stripe
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
import pytz

from Account.models import UserProfile
# from Client.models import MerchantAccount
from Company.models.PaymentInfo import PaymentInfo
from Company.models.CompanyAddressModel import CompanyAddressModel
from Company.models.Package import Package
from django.conf import settings


def get_us_timezones():
    return [
        (timezone, timezone) for timezone in pytz.country_timezones.get("US")
    ]


# def date_formats():
#     date_format='MM-DD-YYYY'
#     return date_format

class CompanyPackage(models.Model):
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL)
    started_at = models.DateTimeField(null=True, blank=False)
    ends_at = models.DateTimeField(null=True, blank=False)
    trail_ends_at = models.DateTimeField(null=True, blank=False)
    is_on_trail = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return self.package.__str__()

    def renew(self, commit=True):
        now = datetime.datetime.now()
        self.started_at = now
        if self.package.pricing_duration == self.package.MONTHLY:
            self.ends_at = now + relativedelta(months=1)
        elif self.package.pricing_duration == self.package.YEARLY:
            self.ends_at = now + relativedelta(years=1)
        if commit:
            self.save()

    def set_on_trail(self, commit=True):
        self.is_on_trail = True
        now = datetime.datetime.now()
        self.trail_ends_at = now + relativedelta(days=settings.LC_TRAIL_PERIOD)
        if commit:
            self.save()

    def end_trail(self, commit=True):
        self.is_on_trail = False
        if commit:
            self.save()


class CompanyProfileModel(models.Model):
    userprofile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(CompanyAddressModel, blank=True, null=True, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=False, null=True)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    distance_unit = models.CharField(max_length=50, blank=False, null=True)
    currency = models.CharField(max_length=10, blank=False, null=True)
    timezone = models.CharField(max_length=100, null=True, blank=True, choices=get_us_timezones())
    date_format = models.CharField(max_length=50, blank=True, null=True)
    gratuity_baseline = models.CharField(max_length=50, blank=True, null=True)
    fuel_surcharge = models.CharField(max_length=50, blank=True, null=True)
    sales_tax = models.CharField(max_length=50, blank=True, null=True)
    company_package = models.ForeignKey(CompanyPackage, null=True, blank=True, on_delete=models.SET_NULL)
    card_details = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE, null=True, blank=True)
    merchant_account = models.ForeignKey("Client.MerchantAccount", null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.company_name

    @property
    def full_name(self):
        return self.userprofile.user.get_full_name()

    @property
    def email(self):
        return self.userprofile.user.email
